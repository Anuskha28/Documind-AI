from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import UPLOAD_DIR
from app.services.ingestion import extract_pdf_pages, chunk_text
from app.services.vector_store import add_documents

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum is 10 MB.")

    destination = UPLOAD_DIR / f"{uuid4().hex}_{Path(file.filename).name}"
    destination.write_bytes(content)

    try:
        pages = extract_pdf_pages(destination)
        items = []

        for page in pages:
            chunks = chunk_text(page["text"])

            for chunk_number, chunk in enumerate(chunks, start=1):
                items.append({
                    "filename": file.filename,
                    "page": page["page"],
                    "chunk": chunk_number,
                    "text": chunk
                })

        if not items:
            raise ValueError("No extractable text found in PDF.")

        add_documents(items)

        return {
            "message": "Document indexed successfully.",
            "filename": file.filename,
            "chunks_added": len(items)
        }

    except Exception as exc:
        if destination.exists():
            destination.unlink()
        raise HTTPException(status_code=500, detail=str(exc))
