# 🌱 Single Plant Smart Agriculture — Web System

Sistem web untuk prototipe IoT Single Plant Smart Agriculture.
Menampung data presisi tinggi sebagai ground truth model Deep Learning, menyediakan dasbor monitoring, dan kendali aktuator penyiraman.

## Tech Stack

| Layer | Teknologi |
|---|---|
| Backend + AI | FastAPI (Python) |
| Frontend | React + Vite |
| Database | PostgreSQL |
| Protokol IoT | HTTP POST |
| Tunnel | Ngrok / Cloudflare Tunnel |

## Struktur Direktori

```
├── backend/          # FastAPI server + ML inference
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── middleware/
│   │   └── ml/
│   ├── static/
│   │   └── uploads/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/         # React + Vite dashboard
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── context/
│   │   └── utils/
│   └── package.json
│
└── README.md
```

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
