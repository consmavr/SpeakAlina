# 🎧 SpeakAlina

This app allows you to upload audio or video files and get transcribed text using OpenAI's Whisper model.
It includes a Flask backend and a React (Vite) frontend, served together as one deployable app.

---

## 🧱 Project Structure

```
SpeakAlina/
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

### Integrate Frontend into Backend

```bash
# From root directory
npm run build
cp -r frontend/dist backend/static
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
