import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [directory, setDirectory] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleScan = async () => {
    setLoading(true);
    setError("");
    setFiles([]);
    try {
      const response = await axios.post("http://127.0.0.1:5000/files/scan", {
        directory,
        exclude_hidden: true,
        exclude_pyc: true,
        exclude_init: true,
        sort_by: "file_size",
        sort_order: "desc",
      });
      if (response.data && response.data.length > 0) {
        setFiles(response.data);
      } else {
        setError("No files found in the selected directory.");
      }
    } catch (err) {
      setError("Error scanning the directory. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const formatSize = (bytes) => {
    if (bytes >= 1024 * 1024 * 1024) {
      return (bytes / (1024 * 1024 * 1024)).toFixed(2) + " GB";
    } else if (bytes >= 1024 * 1024) {
      return (bytes / (1024 * 1024)).toFixed(2) + " MB";
    } else if (bytes >= 1024) {
      return (bytes / 1024).toFixed(2) + " KB";
    } else {
      return bytes + " Bytes";
    }
  };

  const exportToCSV = () => {
    const csvContent = [
      ["File Path", "Size", "Last Accessed"],
      ...files.map((file) => [
        file.file_path,
        formatSize(file.file_size),
        file.last_access_time,
      ]),
    ]
      .map((e) => e.join(","))
      .join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "scanned_files.csv";
    link.click();
  };

  return (
    <div className="App">
      <h1>File Scanner</h1>
      <div className="input-container">
        <input
          type="text"
          value={directory}
          placeholder="Enter directory path"
          onChange={(e) => setDirectory(e.target.value)}
        />
        <button onClick={handleScan} disabled={loading}>
          {loading ? "Scanning..." : "Scan Directory"}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="table-container">
        {loading && <div className="spinner">Loading...</div>}
        {!loading && files.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>File Path</th>
                <th>Size</th>
                <th>Last Accessed</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file, index) => (
                <tr key={index}>
                  <td>{file.file_path}</td>
                  <td>{formatSize(file.file_size)}</td>
                  <td>{file.last_access_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      {files.length > 0 && (
        <button onClick={exportToCSV}>Export to CSV</button>
      )}
    </div>
  );
}

export default App;
