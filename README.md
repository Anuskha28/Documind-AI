# DocuMind AI — RAG Document Assistant

Full-stack RAG MVP using React, FastAPI, PDF extraction, Sentence Transformers, FAISS and Gemini.

## Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Put your Gemini API key in .env
uvicorn app.main:app --reload
```

Backend: http://localhost:8000

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

This is an interview/portfolio MVP. Production improvements should include authentication, document-level access control, persistent storage, background ingestion, rate limiting, evaluation, monitoring and stronger security.
