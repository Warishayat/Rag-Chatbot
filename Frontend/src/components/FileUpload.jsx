import { useState, useRef } from 'react';
import axios from 'axios';
import { UploadCloud, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({ onFileUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle, uploading, success, error
  const [errorMessage, setErrorMessage] = useState('');
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const extension = selectedFile.name.split('.').pop().toLowerCase();
    
    if (!['pdf', 'docx', 'txt'].includes(extension)) {
      setStatus('error');
      setErrorMessage('Please upload a PDF, DOCX, or TXT file.');
      return;
    }
    
    setFile(selectedFile);
    setStatus('idle');
    setErrorMessage('');
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setStatus('uploading');
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus('success');
      onFileUploadSuccess(response.data.filename);
    } catch (error) {
      setStatus('error');
      setErrorMessage(error.response?.data?.detail || 'Upload failed. Please try again.');
    }
  };

  return (
    <div className="upload-container glass-panel animate-fade-in">
      <h2 className="section-title">
        <span className="gradient-text">Document</span> Source
      </h2>
      <p className="section-subtitle">Upload your context file to begin the conversation.</p>
      
      <form 
        className={`upload-zone ${dragActive ? 'drag-active' : ''} ${file ? 'has-file' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        
        {!file ? (
          <div className="upload-prompt">
            <UploadCloud size={48} className="upload-icon" />
            <p>Drag and drop your file here or <span>click to browse</span></p>
            <span className="file-types">Supports: PDF, DOCX, TXT</span>
          </div>
        ) : (
          <div className="file-info">
            <FileText size={32} className="file-icon" />
            <span className="filename">{file.name}</span>
            <span className="filesize">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
          </div>
        )}
      </form>

      {status === 'error' && (
        <div className="status-message error animate-fade-in">
          <AlertCircle size={18} />
          <span>{errorMessage}</span>
        </div>
      )}

      {status === 'success' && (
        <div className="status-message success animate-fade-in">
          <CheckCircle size={18} />
          <span>File ready for chat!</span>
        </div>
      )}

      <button 
        className={`upload-button ${!file || status === 'uploading' || status === 'success' ? 'disabled' : ''}`}
        onClick={handleUpload}
        disabled={!file || status === 'uploading' || status === 'success'}
      >
        {status === 'uploading' ? (
          <><Loader2 className="spinner" size={18} /> Processing...</>
        ) : status === 'success' ? (
          'Uploaded Successfully'
        ) : (
          'Process Document'
        )}
      </button>
    </div>
  );
};

export default FileUpload;
