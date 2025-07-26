# 🎧 SpeakAlina  
_Transcribing stuff made simple_

This app transcribes audio files via a Python backend and a React (Vite) frontend. The backend handles transcription, while the frontend provides an interface for users to upload audio and view transcripts.

---

## 🧱 Project Structure

```
mnemo/
├── backend/            # Python backend (Flask/FastAPI)
├── frontend/           # React (Vite) frontend
├── .env                # Environment variables for backend
└── README.md           # This file
```

---

## 🚀 Build & Run Locally with Docker

### 1️⃣ Backend: Python (Port 8082)

#### 🔧 Build the Docker image:
```bash
docker build -t audio-transcriber-backend .
```

#### ▶️ Run the backend container:
```bash
docker run -p 8082:8082 --env-file .env audio-transcriber-backend
```

> Make sure the `.env` file contains necessary environment variables such as API keys, if required.

---

### 2️⃣ Frontend: React (Vite)

#### 📦 Build the Docker image:
```bash
cd frontend
docker build -t audio-frontend .
```

> You can extend this with a separate Dockerfile to run the frontend on a static hosting server like Nginx.

---

## 🧪 Development (without Docker)

### Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8082
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

---


## 📬 API

**POST** `/transcribe`

| Field | Type   | Description          |
|-------|--------|----------------------|
| file  | `audio` | Audio file to transcribe |

**Response:**
```json
{
  "transcript": "Your transcribed text here"
}
```

---

## ✅ TODO

- [ ] Add tests
- [ ] Save transcript as downloadable file
- [ ] Multi-language support
