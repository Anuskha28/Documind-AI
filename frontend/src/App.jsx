import { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000/api";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  async function uploadFile() {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setUploadStatus("Indexing document...");

    try {
      const res = await axios.post(`${API}/upload`, formData);
      setUploadStatus(
        `${res.data.filename} indexed: ${res.data.chunks_added} chunks`
      );
    } catch (error) {
      setUploadStatus(error.response?.data?.detail || "Upload failed.");
    }
  }

  async function askQuestion(e) {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const res = await axios.post(`${API}/chat`, {
        question,
        top_k: 5
      });

      setAnswer(res.data.answer);
      setSources(res.data.sources || []);
    } catch (error) {
      setAnswer(error.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <header>
        <h1>DocuMind AI</h1>
        <p>Ask questions about your uploaded documents using RAG.</p>
      </header>

      <section className="card">
        <h2>1. Upload a PDF</h2>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={uploadFile} disabled={!file}>
          Upload & Index
        </button>
        {uploadStatus && <p className="status">{uploadStatus}</p>}
      </section>

      <section className="card">
        <h2>2. Ask a question</h2>
        <form onSubmit={askQuestion}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. What is the company's leave policy?"
            rows="4"
          />
          <button type="submit" disabled={loading}>
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>
      </section>

      {answer && (
        <section className="card">
          <h2>Answer</h2>
          <div className="answer">{answer}</div>

          <h3>Retrieved Sources</h3>
          {sources.map((source, index) => (
            <div
              className="source"
              key={`${source.filename}-${source.page}-${index}`}
            >
              <strong>{source.filename}</strong>
              <span>Page {source.page}</span>
              <span>Score {source.score}</span>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}
