import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setTranscript("");
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);
      const isProductionEnv = import.meta.env.VITE_ENV_TYPE === "production ";
      const apiUrl = isProductionEnv
        ? window.location.href
        : "http://localhost:8082/";
      const response = await fetch(apiUrl + "transcribe", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const text = await response.text();
      setTranscript(text);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      setError(err.message || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(transcript);
  };

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        width: "100vw",
      }}
    >
      <header style={{
        marginBottom: "1.5rem", height: "100px"
      }}>
        <img src="/logo.png" alt="img" height={100} />
      </header>

      <div style={{ marginBottom: "2rem" }}>
        <input type="file" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          disabled={loading || !file}
          style={{
            marginLeft: "1rem",
            padding: "0.5rem 1rem",
            fontSize: "1rem",
            cursor: loading || !file ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Processing..." : "Upload & Transcribe"}
        </button>
      </div>

      {error && (
        <div style={{ color: "red", marginBottom: "1rem" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {transcript && (
        <button
          onClick={handleCopy}
          style={{
            marginTop: "1rem",
            padding: "0.5rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#4A90E2",
            color: "white",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
          title="Copy transcript to clipboard"
        >
          Copy Text
        </button>
      )}
      {transcript && (
        <div
          style={{
            marginTop: "1rem",
            padding: "1rem",
            border: "1px solid #ddd",
            borderRadius: 6,
            backgroundColor: "#f9f9f9",
            color: "#333",
            fontSize: "1rem",
            lineHeight: "1.5",
            whiteSpace: "pre-wrap",
            textAlign: "left",
          }}
        >
          {transcript}
        </div>
      )}


    </div>
  );
}
