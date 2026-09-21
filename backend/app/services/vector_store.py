import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import INDEX_DIR

MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)

INDEX_PATH = INDEX_DIR / "index.faiss"
META_PATH = INDEX_DIR / "metadata.json"

def embed_texts(texts):
    vectors = _model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True
    )
    return vectors.astype("float32")

def load_store():
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return None, []

    return (
        faiss.read_index(str(INDEX_PATH)),
        json.loads(META_PATH.read_text(encoding="utf-8"))
    )

def add_documents(items):
    texts = [item["text"] for item in items]
    vectors = embed_texts(texts)

    index, metadata = load_store()

    if index is None:
        index = faiss.IndexFlatIP(vectors.shape[1])

    index.add(vectors)
    metadata.extend(items)

    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def search(query: str, top_k: int = 5):
    index, metadata = load_store()

    if index is None or index.ntotal == 0:
        return []

    query_vector = embed_texts([query])
    k = min(top_k, index.ntotal)
    scores, indices = index.search(query_vector, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        item = metadata[int(idx)].copy()
        item["score"] = float(score)
        results.append(item)

    return results
