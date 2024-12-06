import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [directory, setDirectory] = useState("");
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [extensions, setExtensions] = useState("");
  const [searchedExtensions, setSearchedExtensions] = useState([]);

  useEffect(() => {
    fetchExtensions();
  }, []);

  const fetchExtensions = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/files/extensions/details");
      setSearchedExtensions(response.data);
    } catch (error) {
      console.error("Error fetching extensions:", error);
    }
  };

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
        extensions: extensions ? extensions.split(",").map((ext) => ext.trim()) : null, // Convert to array or null
      };
      const response = await axios.post("http://127.0.0.1:5000/files/scan", payload);
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
      {files.length > 0 && <button onClick={exportToCSV}>Export to CSV</button>}
      <div className="extensions-container">
        <h2>Searched Extensions</h2>
        {Object.keys(searchedExtensions).length > 0 ? (
          <ul>
            {Object.entries(searchedExtensions).map(([ext, files]) => (
              <li key={ext}>
                <strong>{ext}:</strong>
                <ul>
                  {files.map((file, index) => (
                    <li key={index}>{file}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        ) : (
          <p>No extensions searched yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;
