from pathlib import Path
from pypdf import PdfReader

def extract_pdf_pages(path: Path):
    reader = PdfReader(str(path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())

        if text:
            pages.append({"page": page_number, "text": text})

    return pages

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = end - overlap

    return chunks
