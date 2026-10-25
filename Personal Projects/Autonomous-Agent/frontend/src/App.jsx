import { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";
// Generation can take several minutes with local models; fail rather than hang forever.
const REQUEST_TIMEOUT_MS = 10 * 60 * 1000;

function App() {
  const [request, setRequest] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const submit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        `${API_BASE_URL}/agent`,
        { request },
        { timeout: REQUEST_TIMEOUT_MS, maxRedirects: 0 },
      );
      setResult(response.data);
    } catch (submissionError) {
      const detail = submissionError.response?.data?.detail;
      if (submissionError.code === "ECONNABORTED") {
        setError("The request timed out. Please try again.");
      } else if (!submissionError.response) {
        setError("Unable to reach the API. Check that the backend is running.");
      } else {
        setError(
          typeof detail === "string"
            ? detail
            : detail?.detail || "The request failed. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const assumptions = result?.plan?.assumptions ?? [];

  return (
    <main>
      <h1>Autonomous Agent</h1>
      <p>Generate a business document via local AI</p>

      <textarea
        value={request}
        onChange={(event) => setRequest(event.target.value)}
        placeholder="Create a business proposal for a mid-sized logistics company..."
      />

      <button
        className={loading ? "button-disabled" : ""}
        disabled={loading}
        onClick={submit}
        type="button"
      >
        {loading && <span aria-label="Loading" className="spinner" />}
        Generate Document
      </button>

      {loading && (
        <p className="status-message">
          Agent is planning, writing, and reflecting... (this may take 2-5 minutes)
        </p>
      )}

      {error && <div className="error">Error: {error}</div>}

      {result && (
        <section className="card">
          <h2>Document Generated</h2>
          <p>{result.summary}</p>

          {assumptions.length > 0 && (
            <div className="assumptions">
              <h3>Agent Assumptions</h3>
              <ul>
                {assumptions.map((assumption) => (
                  <li key={assumption}>{assumption}</li>
                ))}
              </ul>
            </div>
          )}

          <a
            className="download-button"
            href={`${API_BASE_URL}${result.download_url}`}
            rel="noreferrer"
            target="_blank"
          >
            Download Word Document
          </a>
        </section>
      )}
    </main>
  );
}

export default App;
