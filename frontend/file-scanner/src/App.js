import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [files, setFiles] = useState([]);
  const [directory, setDirectory] = useState('');

  const handleFileSelect = (event) => {
    const selectedDirectory = event.target.files[0]?.webkitRelativePath.split('/')[0];
    setDirectory(selectedDirectory);
  };

  const handleScan = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/files/scan', {
        directory: directory || '/path/to/your/directory', // Use selected directory or default
        exclude_hidden: true,
        exclude_pyc: true,
        exclude_init: true,
      });
      setFiles(response.data);
    } catch (error) {
      console.error("Error scanning files:", error);
    }
  };

  return (
    <div>
      <h1>File Scanner</h1>
      <input
        type="file"
        webkitdirectory="true"
        directory="true"
        onChange={handleFileSelect}
      />
      <button onClick={handleScan}>Scan Directory</button>
      <div>
        <h2>Scanned Files:</h2>
        <pre>{JSON.stringify(files, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
