import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, User, Bot, Loader2, Sparkles, BookOpen } from 'lucide-react';
import './ChatInterface.css';

const ChatInterface = ({ filename, sessionId }) => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I am your AI assistant. I have processed your document. What would you like to know?',
      timestamp: new Date().toISOString(),
      sources: []
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !filename || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/chat', {
        query: userMessage.content,
        filename: filename,
        session_id: sessionId
      });

      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources || [],
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request.',
        isError: true,
        timestamp: new Date().toISOString(),
        sources: []
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container glass-panel animate-fade-in">
      <div className="chat-header">
        <div className="header-title">
          <Sparkles className="header-icon" size={24} />
          <h2>AI Assistant</h2>
        </div>
        <div className="session-info">
          <span>Active File: <strong>{filename}</strong></span>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.role}`}>
            <div className={`message-avatar ${msg.role}`}>
              {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>
            <div className={`message-content-group ${msg.role}`}>
              <div className={`message-bubble ${msg.role} ${msg.isError ? 'error' : ''}`}>
                <p>{msg.content}</p>
                <span className="timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              
              {/* Sources / Metadata Display */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources-container">
                  <div className="sources-header">
                    <BookOpen size={12} />
                    <span>Sources used:</span>
                  </div>
                  <div className="sources-list">
                    {msg.sources.map((source, index) => {
                      // Extract useful metadata (page, source file, etc.)
                      const pageNum = source.page !== undefined ? `Page ${source.page}` : '';
                      const sourceName = source.source ? source.source.split('\\').pop().split('/').pop() : 'Document';
                      
                      return (
                        <span key={index} className="source-badge">
                          {sourceName} {pageNum && `- ${pageNum}`}
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="message-avatar assistant">
              <Bot size={18} />
            </div>
            <div className="message-bubble assistant loading">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your document..."
          disabled={isLoading || !filename}
        />
        <button 
          type="submit" 
          disabled={!input.trim() || isLoading || !filename}
          className="send-button"
        >
          {isLoading ? <Loader2 className="spinner" size={20} /> : <Send size={20} />}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
