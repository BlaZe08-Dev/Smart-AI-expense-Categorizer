import { useState } from "react";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

const handleUpload = async () => {
  if (!file) {
    setError("Please select a PDF file");
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

    // ✅ ADD THESE LINES HERE 👇
    localStorage.setItem("analytics", JSON.stringify(data.analytics));
    localStorage.setItem("transactions", JSON.stringify(data.transactions));
    localStorage.setItem("transactions_count", data.transactions_count);

    // Redirect
    window.location.href = "/dashboard";
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};


  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1>AI Smart Expense Analyzer</h1>
        <p>Upload your bank statement PDF</p>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <input
          type="password"
          placeholder="PDF Password (optional)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>

        {error && <p style={{ color: "red" }}>{error}</p>}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a",
    color: "#fff",
  },
  card: {
    background: "#1e293b",
    padding: 30,
    borderRadius: 10,
    width: 350,
    display: "flex",
    flexDirection: "column",
    gap: 15,
  },
};

export default UploadPage;
