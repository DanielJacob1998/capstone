import React, { useState } from 'react';
import './FileUpload.css'; // Include this file for styling.

const FileUpload = ({ onUploadComplete }) => {
    const [files, setFiles] = useState([]);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadMessage, setUploadMessage] = useState('');

    const validFileTypes = ['text/csv', 'text/calendar'];
    const maxFileSizeMB = 5; // Maximum file size in MB

    const handleFileChange = (event) => {
        const selectedFiles = Array.from(event.target.files);
        const filteredFiles = selectedFiles.filter((file) => {
            if (!validFileTypes.includes(file.type)) {
                setUploadMessage(`Invalid file type: ${file.name}`);
                return false;
            }
            if (file.size > maxFileSizeMB * 1024 * 1024) {
                setUploadMessage(`File too large: ${file.name}`);
                return false;
            }
            return true;
        });

        setFiles(filteredFiles);
        setUploadMessage('');
    };

    const handleUpload = async () => {
        if (!files.length) {
            setUploadMessage('Please select at least one file.');
            return;
        }

        setIsUploading(true);
        setUploadMessage('');
        setUploadProgress(0);

        try {
            const formData = new FormData();
            files.forEach((file) => formData.append('files', file));

            const response = await fetch('http://127.0.0.1:5000/files/parse-finance', {
                method: 'POST',
                body: formData,
                onUploadProgress: (progressEvent) => {
                    const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
                    setUploadProgress(progress);
                },
            });

            const result = await response.json();

            if (response.ok) {
                setUploadMessage('Files uploaded successfully!');
                onUploadComplete(result);
            } else {
                setUploadMessage(`Error: ${result.error || 'Failed to upload files.'}`);
            }
        } catch (error) {
            setUploadMessage(`Error: ${error.message}`);
        } finally {
            setIsUploading(false);
            setUploadProgress(0);
        }
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        event.stopPropagation();
    };

    const handleDrop = (event) => {
        event.preventDefault();
        event.stopPropagation();

        const droppedFiles = Array.from(event.dataTransfer.files);
        const filteredFiles = droppedFiles.filter((file) => {
            if (!validFileTypes.includes(file.type)) {
                setUploadMessage(`Invalid file type: ${file.name}`);
                return false;
            }
            if (file.size > maxFileSizeMB * 1024 * 1024) {
                setUploadMessage(`File too large: ${file.name}`);
                return false;
            }
            return true;
        });

        setFiles(filteredFiles);
        setUploadMessage('');
    };

    const reset = () => {
        setFiles([]);
        setUploadMessage('');
        setUploadProgress(0);
    };

    return (
        <div className="file-upload">
            <h2>Upload Files</h2>
            <div
                className="file-dropzone"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                aria-label="Drag and drop files here or click to upload."
            >
                <input
                    type="file"
                    multiple
                    onChange={handleFileChange}
                    disabled={isUploading}
                    aria-label="Select files to upload"
                />
                {files.length === 0 ? (
                    <p>Drag and drop files here, or click to select files.</p>
                ) : (
                    <ul>
                        {files.map((file, index) => (
                            <li key={index}>
                                {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            {uploadProgress > 0 && (
                <div className="progress-bar">
                    <div
                        className="progress-bar-fill"
                        style={{ width: `${uploadProgress}%` }}
                    >
                        {uploadProgress}%
                    </div>
                </div>
            )}
            <button onClick={handleUpload} disabled={isUploading || files.length === 0}>
                {isUploading ? 'Uploading...' : 'Upload'}
            </button>
            <button onClick={reset} disabled={isUploading}>
                Reset
            </button>
            {uploadMessage && <p className="upload-message">{uploadMessage}</p>}
        </div>
    );
};

export default FileUpload;
