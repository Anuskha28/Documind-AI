from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.vector_store import search
from app.services.llm import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=10)

@router.post("/chat")
def chat(request: ChatRequest):
    try:
        results = search(request.question, request.top_k)

        if not results:
            return {
                "answer": "No indexed documents are available yet. Please upload a PDF first.",
                "sources": []
            }

        answer = generate_answer(request.question, results)

        sources = [
            {
                "filename": item["filename"],
                "page": item["page"],
                "score": round(item["score"], 4)
            }
            for item in results
        ]

        return {"answer": answer, "sources": sources}

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
