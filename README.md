# mnemo
Transcribing stuff


🚀 Build & Run the Container Locally

1. Build the image

docker build -t audio-transcriber-backend .

2. Run the container with .env passed

docker run -p 8082:8082 --env-file .env audio-transcriber-backend

cd frontend
docker build -t audio-frontend .
