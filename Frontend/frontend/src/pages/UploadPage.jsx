import { useState } from "react";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select or drop a PDF file");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    if (password) formData.append("password", password);

    try {
      const response = await fetch("http://127.0.0.1:8000/pdf/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || data.status !== "success") {
        throw new Error(data.message || "Upload failed");
      }

      localStorage.setItem("analytics", JSON.stringify(data.analytics));
      localStorage.setItem("transactions", JSON.stringify(data.transactions));
      localStorage.setItem("transactions_count", data.transactions_count);

      window.location.href = "/dashboard";
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const dropped = e.dataTransfer.files[0];
    if (dropped && dropped.type === "application/pdf") {
      setFile(dropped);
      setError(null);
    } else {
      setError("Only PDF files are supported");
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card} className="fadeIn">
        <h1 style={styles.title}>Smart AI Expense Analyzer</h1>
        <p style={styles.subtitle}>Drag & drop your bank statement PDF</p>

        {/* DRAG DROP */}
        <div
          style={{
            ...styles.dropZone,
            ...(dragActive ? styles.dropActive : {}),
          }}
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => document.getElementById("fileInput").click()}
        >
          <input
            id="fileInput"
            type="file"
            accept=".pdf"
            hidden
            onChange={(e) => setFile(e.target.files[0])}
          />

          {file ? (
            <p className="scaleIn">📄 {file.name}</p>
          ) : (
            <p>Drop PDF here or click to browse</p>
          )}
        </div>

        <input
          type="password"
          placeholder="PDF Password (optional)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          style={styles.button}
        >
          {loading ? <span className="spinner" /> : "Upload & Analyze"}
        </button>

        {error && <p style={styles.error}>{error}</p>}
      </div>

      {/* CSS ANIMATIONS */}
      <style>
        {`
          .fadeIn {
            animation: fadeUp 0.6s ease-out;
          }

          .scaleIn {
            animation: scaleIn 0.3s ease;
          }

          .spinner {
            width: 18px;
            height: 18px;
            border: 3px solid rgba(0,0,0,0.2);
            border-top: 3px solid #020617;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            display: inline-block;
          }

          @keyframes fadeUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          @keyframes scaleIn {
            from {
              transform: scale(0.95);
            }
            to {
              transform: scale(1);
            }
          }

          @keyframes spin {
            to {
              transform: rotate(360deg);
            }
          }
        `}
      </style>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    width: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #020617, #0f172a)",
    padding: "clamp(16px, 5vw, 48px)",
  },

  card: {
    width: "100%",
    maxWidth: 420,
    background: "#020617",
    padding: "clamp(20px, 4vw, 32px)",
    borderRadius: 16,
    display: "flex",
    flexDirection: "column",
    gap: 16,
    boxShadow: "0 20px 40px rgba(0,0,0,0.4)",
  },

  title: {
    textAlign: "center",
  },

  subtitle: {
    textAlign: "center",
    opacity: 0.8,
    fontSize: 14,
  },

  dropZone: {
    border: "2px dashed #334155",
    borderRadius: 12,
    padding: 24,
    textAlign: "center",
    cursor: "pointer",
    transition: "all 0.25s ease",
    fontSize: 14,
  },

  dropActive: {
    borderColor: "#38bdf8",
    background: "#020617",
    transform: "scale(1.02)",
  },

  input: {
    padding: 12,
    borderRadius: 8,
    border: "none",
    outline: "none",
    fontSize: 14,
  },

  button: {
    padding: 12,
    borderRadius: 10,
    border: "none",
    background: "#38bdf8",
    color: "#020617",
    fontWeight: 600,
    fontSize: 15,
    cursor: "pointer",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: 44,
  },

  error: {
    color: "#f87171",
    textAlign: "center",
    fontSize: 14,
  },
};

export default UploadPage;