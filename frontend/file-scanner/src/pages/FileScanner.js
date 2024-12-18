import React, { useState } from "react";
import axios from "axios";
import "../App.css";

function App() {
  const [directory, setDirectory] = useState("");
  const [extensions, setExtensions] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sortBy, setSortBy] = useState("file_name");
  const [sortOrder, setSortOrder] = useState("asc");

  const handleScan = async () => {
    setLoading(true);
    setError("");
    setFiles([]);
    try {
      const payload = {
        directory,
        exclude_hidden: true,
        exclude_pyc: true,
        exclude_init: true,
        extensions: extensions ? extensions.split(",").map((ext) => ext.trim()) : null,
      };

      const response = await axios.post("http://127.0.0.1:5000/files/scan", payload);

      if (response.data && response.data.length > 0) {
        const filesWithNames = response.data.map((file) => ({
          ...file,
          file_name: file.file_name || file.file_path?.split("/").pop() || "Unknown",
        }));
        setFiles(filesWithNames);
      }
    } catch (err) {
      setError("Error scanning the directory. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (column) => {
    const nextSortOrder = sortBy === column && sortOrder === "asc" ? "desc" : "asc";
    setSortBy(column);
    setSortOrder(nextSortOrder);

    const sortedFiles = [...files].sort((a, b) => {
      const aValue = a[column] || "";
      const bValue = b[column] || "";

      if (column === "file_size") {
        return nextSortOrder === "asc" ? aValue - bValue : bValue - aValue;
      } else if (column.includes("date")) {
        const dateA = new Date(aValue);
        const dateB = new Date(bValue);
        return nextSortOrder === "asc" ? dateA - dateB : dateB - dateA;
      } else {
        return nextSortOrder === "asc"
          ? aValue.toLowerCase().localeCompare(bValue.toLowerCase())
          : bValue.toLowerCase().localeCompare(aValue.toLowerCase());
      }
    });

    setFiles(sortedFiles);
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
        <input
          type="text"
          value={extensions}
          placeholder="Enter extensions (e.g., .txt,.jpg)"
          onChange={(e) => setExtensions(e.target.value)}
        />
        <button onClick={handleScan} disabled={loading}>
          {loading ? "Scanning..." : "Scan Directory"}
        </button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      {files.length === 0 && !loading && <p>No files found.</p>}
      {files.length > 0 && (
        <table>
          <thead>
            <tr>
              <th onClick={() => handleSort("file_name")}>
                File Name {sortBy === "file_name" && (sortOrder === "asc" ? "▲" : "▼")}
              </th>
              <th onClick={() => handleSort("file_size")}>
                File Size {sortBy === "file_size" && (sortOrder === "asc" ? "▲" : "▼")}
              </th>
              <th onClick={() => handleSort("date_created")}>
                Date Created {sortBy === "date_created" && (sortOrder === "asc" ? "▲" : "▼")}
              </th>
              <th onClick={() => handleSort("date_modified")}>
                Date Modified {sortBy === "date_modified" && (sortOrder === "asc" ? "▲" : "▼")}
              </th>
              <th onClick={() => handleSort("date_accessed")}>
                Date Accessed {sortBy === "date_accessed" && (sortOrder === "asc" ? "▲" : "▼")}
              </th>
            </tr>
          </thead>
          <tbody>
            {files.map((file, index) => (
              <tr key={index}>
                <td>{file.file_name}</td>
                <td>{formatSize(file.file_size)}</td>
                <td>{file.date_created}</td>
                <td>{file.date_modified}</td>
                <td>{file.date_accessed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;

