import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [directory, setDirectory] = useState("");
  const [fileDetails, setFileDetails] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // New state variables for sorting options
  const [sortBy, setSortBy] = useState("file_name"); // Default to sorting by file name
  const [sortOrder, setSortOrder] = useState("asc"); // Default to ascending order

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
        extensions: fileDetails ? fileDetails.split(",").map((detail) => detail.trim()) : null,
        sort_by: sortBy,
        sort_order: sortOrder,
      };

      const response = await axios.post("http://127.0.0.1:5000/files/scan", payload);
      if (response.data && response.data.length > 0) {
        const sortedFiles = response.data.sort((a, b) => {
          if (sortBy.includes("date")) {
            // Parse dates for proper comparison
            const dateA = new Date(a[sortBy]);
            const dateB = new Date(b[sortBy]);
            return sortOrder === "asc" ? dateA - dateB : dateB - dateA;
          } else if (sortBy === "file_size") {
            return sortOrder === "asc" ? a.file_size - b.file_size : b.file_size - a.file_size;
          } else {
            // Default to lexicographical sorting (e.g., for file_name)
            return sortOrder === "asc"
              ? a[sortBy].localeCompare(b[sortBy])
              : b[sortBy].localeCompare(a[sortBy]);
          }
        });
        setFiles(sortedFiles);
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
          value={fileDetails}
          placeholder="Enter filters (e.g., .txt,.jpg)"
          onChange={(e) => setFileDetails(e.target.value)}
        />
        <div className="sorting-container">
          <label>Sort By:</label>
          <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
            <option value="file_name">File Name</option>
            <option value="file_size">File Size</option>
            <option value="date_created">Date Created</option>
            <option value="date_modified">Date Modified</option>
            <option value="date_accessed">Date Accessed</option>
          </select>
          <label>Order:</label>
          <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
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
                <th>File Size</th>
                <th>Date Created</th>
                <th>Date Modified</th>
                <th>Date Accessed</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file, index) => (
                <tr key={index}>
                  <td>{file.file_path}</td>
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
    </div>
  );
}

export default App;
