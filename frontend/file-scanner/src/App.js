import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [directory, setDirectory] = useState("");
  const [extensions, setExtensions] = useState(""); // Fixed: Declare extensions state
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  // eslint-disable-next-line
  const [sortBy, setSortBy] = useState("file_name"); // Default to sorting by file name
  // eslint-disable-next-line
  const [sortOrder, setSortOrder] = useState("asc"); // Default to ascending order

  const [dateCreatedRange, setDateCreatedRange] = useState({ start: "", end: "" });
  const [dateModifiedRange, setDateModifiedRange] = useState({ start: "", end: "" });
  const [dateAccessedRange, setDateAccessedRange] = useState({ start: "", end: "" });

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
        sort_by: sortBy,
        sort_order: sortOrder,
        date_created_range:
          dateCreatedRange.start && dateCreatedRange.end
            ? [dateCreatedRange.start, dateCreatedRange.end]
            : null,
        date_modified_range:
          dateModifiedRange.start && dateModifiedRange.end
            ? [dateModifiedRange.start, dateModifiedRange.end]
            : null,
        date_accessed_range:
          dateAccessedRange.start && dateAccessedRange.end
            ? [dateAccessedRange.start, dateAccessedRange.end]
            : null,
      };

      const response = await axios.post("http://127.0.0.1:5000/files/scan", payload);
      setFiles(response.data || []);
    } catch (err) {
      console.error("Error details:", err); // Log error for debugging
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
          value={extensions}
          placeholder="Enter extensions (e.g., .txt,.jpg)"
          onChange={(e) => setExtensions(e.target.value)}
        />
        <div>
          <label>Date Created Range:</label>
          <input
            type="date"
            value={dateCreatedRange.start}
            onChange={(e) =>
              setDateCreatedRange({ ...dateCreatedRange, start: e.target.value })
            }
          />
          <input
            type="date"
            value={dateCreatedRange.end}
            onChange={(e) =>
              setDateCreatedRange({ ...dateCreatedRange, end: e.target.value })
            }
          />
        </div>
        <div>
          <label>Date Modified Range:</label>
          <input
            type="date"
            value={dateModifiedRange.start}
            onChange={(e) =>
              setDateModifiedRange({ ...dateModifiedRange, start: e.target.value })
            }
          />
          <input
            type="date"
            value={dateModifiedRange.end}
            onChange={(e) =>
              setDateModifiedRange({ ...dateModifiedRange, end: e.target.value })
            }
          />
        </div>
        <div>
          <label>Date Accessed Range:</label>
          <input
            type="date"
            value={dateAccessedRange.start}
            onChange={(e) =>
              setDateAccessedRange({ ...dateAccessedRange, start: e.target.value })
            }
          />
          <input
            type="date"
            value={dateAccessedRange.end}
            onChange={(e) =>
              setDateAccessedRange({ ...dateAccessedRange, end: e.target.value })
            }
          />
        </div>
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
  );
}

export default App;

