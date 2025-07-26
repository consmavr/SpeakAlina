from flask import Flask, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import os
import subprocess
import math
import tempfile

# Load environment variables
load_dotenv()
api_key = os.getenv("GPT_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)

def convert_to_audio(input_file: Path, output_dir: Path):
    if input_file.suffix.lower() == '.mp4':
        output_file = output_dir / (input_file.stem + '.wav')
    else:
        output_file = output_dir / (input_file.stem + '.mp3')
    subprocess.run(['ffmpeg', '-i', str(input_file), str(output_file)], check=True)
    return output_file

def calculate_bitrate_for_size(target_size_MB, duration_sec):
    target_size_bits = target_size_MB * 8 * 1024 * 1024 - (5 * 1024 * 1024 * 8)
    bitrate = target_size_bits / duration_sec
    return int(bitrate)

def split_file(file_path: Path, output_dir: Path, target_chunk_size_MB=25):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                             'default=noprint_wrappers=1:nokey=1', str(file_path)],
                            text=True, capture_output=True)
    duration_sec = float(result.stdout)
    estimated_bitrate = calculate_bitrate_for_size(target_chunk_size_MB, duration_sec)

    output_pattern = str(output_dir / (file_path.stem + '-%03d.mp3'))
    split_command = [
        'ffmpeg', '-i', str(file_path),
        '-b:a', str(estimated_bitrate),
        '-f', 'segment',
        '-segment_time', str(duration_sec / math.ceil((os.path.getsize(file_path) / (1024 * 1024)) / target_chunk_size_MB)),
        '-c:a', 'libmp3lame',
        output_pattern
    ]
    subprocess.run(split_command, check=True)

def transcribe_file(file_path: Path):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=open(file_path, "rb"),
        response_format="text"
    )
    return transcript

@app.route('/transcribe', methods=['POST'])
def transcribe():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'error': 'No file provided'}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        input_path = tmpdir_path / uploaded_file.filename
        uploaded_file.save(str(input_path))

        try:
            audio_file = convert_to_audio(input_path, tmpdir_path)
            split_file(audio_file, tmpdir_path)

            chunks = sorted(tmpdir_path.glob(f'{audio_file.stem}-*.mp3'))

            combined_text = ""
            for chunk in chunks:
                text = transcribe_file(chunk)
                combined_text += text + " "

            words = combined_text.split()
            formatted_text = '\n'.join([' '.join(words[i:i+20]) for i in range(0, len(words), 20)])

            return Response(formatted_text, mimetype='text/plain')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Serve static React files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    static_path = Path(app.static_folder) / path
    if static_path.exists():
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8082)
