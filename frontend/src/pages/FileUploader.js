// FileUploader Component: Reusable for uploading files
import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

const FileUploader = ({ endpoint, onSuccess, acceptedFormats, label }) => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const fileExtension = selectedFile.name.split('.').pop().toLowerCase();
            if (acceptedFormats.includes(fileExtension)) {
                setFile(selectedFile);
                setMessage('');
            } else {
                setMessage(`Invalid file type. Accepted formats: ${acceptedFormats.join(', ')}`);
                setFile(null);
            }
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a valid file.');
            return;
        }

        setLoading(true);
        setMessage('');
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(endpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setMessage('File uploaded successfully!');
            onSuccess(response.data);
        } catch (error) {
            setMessage(
                error.response?.data?.error || 'An error occurred during file upload.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="file-uploader">
            <label>{label}</label>
            <input type="file" onChange={handleFileChange} />
            {loading && <p>Uploading... Please wait.</p>}
            {message && <p>{message}</p>}
            <button onClick={handleUpload} disabled={loading || !file}>
                Upload
            </button>
        </div>
    );
};

export default FileUploader;
