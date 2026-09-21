# DocuMind AI

Enterprise RAG-based Document Question Answering System

## Features
- PDF document ingestion
- Intelligent text chunking
- Sentence Transformer embeddings
- FAISS vector search
- Semantic retrieval
- Gemini-powered answer generation
- Source/page references
- Hallucination reduction through grounded generation

## Architecture

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Store
 ↓
User Query
 ↓
Query Embedding
 ↓
Similarity Search
 ↓
Top-K Context
 ↓
Gemini LLM
 ↓
Grounded Answer + Sources

## Tech Stack

Frontend:
React + Vite

Backend:
Python + FastAPI

AI:
Gemini
Sentence Transformers
RAG

Vector Database:
FAISS

## How to Run

Backend:
...
 
Frontend:
...

## Project Structure
...

## Future Improvements
- Multi-document retrieval
- Reranking
- Hybrid search
- RAG evaluation
- Agentic routing
- Authentication
- Deployment
