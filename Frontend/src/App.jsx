import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import { Database } from 'lucide-react';

function App() {
  const [sessionId, setSessionId] = useState('');
  const [activeFilename, setActiveFilename] = useState('');

  useEffect(() => {
    // Generate a unique session ID for this user's tab
    setSessionId(uuidv4());
  }, []);

  const handleFileUploadSuccess = (filename) => {
    setActiveFilename(filename);
  };

  return (
    <div className="app-container">
      <div className="sidebar animate-fade-in">
        <div className="brand-header">
          <div className="logo-icon">
            <Database size={28} />
          </div>
          <h1>RAG <span className="gradient-text">Nexus</span></h1>
        </div>
        
        <p className="app-description">
          An intelligent document assistant powered by advanced Retrieval-Augmented Generation.
        </p>

        <FileUpload onFileUploadSuccess={handleFileUploadSuccess} />
        
        <div className="glass-panel info-panel mt-auto">
          <h3>How it works</h3>
          <ol>
            <li>Upload your document (PDF, DOCX, TXT)</li>
            <li>System generates Hybrid Search (Semantic + Keyword) indexes</li>
            <li>Ask questions in natural language</li>
            <li>Get precise answers with context</li>
          </ol>
        </div>
      </div>

      <div className="main-content">
        {!activeFilename ? (
          <div className="empty-state glass-panel animate-fade-in">
            <div className="empty-state-content">
              <Database size={64} className="empty-icon" />
              <h2>Awaiting Document</h2>
              <p>Please upload a document from the sidebar to start the conversation.</p>
            </div>
          </div>
        ) : (
          <ChatInterface filename={activeFilename} sessionId={sessionId} />
        )}
      </div>
    </div>
  );
}

export default App;
