'use client';

import React, { useState, useRef, useEffect } from 'react';
import { taskApi } from '../services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatbotWidgetProps {
  userId: string;
  onTaskUpdate?: () => void; // Callback to refresh tasks when operations are performed
}

const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({ userId, onTaskUpdate }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. You can ask me to manage your tasks using natural language. Try saying "Add a task to buy groceries" or "Show me my tasks".',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API using the taskApi service
      const result = await taskApi.chatWithAssistant(
        userId,
        messages.concat([userMessage]).map(msg => ({ role: msg.role, content: msg.content }))
      );

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: result.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if the response indicates a task operation was performed
      const responseText = result.response.toLowerCase();
      const taskOperationKeywords = ['added', 'deleted', 'completed', 'marked', 'updated', 'removed'];
      const containsTaskOperation = taskOperationKeywords.some(keyword =>
        responseText.includes(keyword)
      );

      // Refresh tasks if callback is provided and a task operation was detected
      if (onTaskUpdate && containsTaskOperation) {
        setTimeout(() => {
          onTaskUpdate();
        }, 1000); // Small delay to allow message to be displayed first
      }
    } catch (error) {
      console.error('Error communicating with chat API:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-widget-inline">
      {/* Chatbot launcher button */}
      <button
        className="chatbot-launcher-inline"
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chatbot container */}
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <h3>✨ AI Task Assistant</h3>
            <button
              className="close-button"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role}`}
              >
                <div className="message-content">{message.content}</div>
                <div className="message-timestamp">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant typing-message">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me to manage your tasks..."
              disabled={isLoading}
              className="chat-input"
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              ➤
            </button>
          </form>
        </div>
      )}

      <style jsx>{`
        .chatbot-widget-inline {
          display: inline-block;
          position: relative;
          margin-left: 10px;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          vertical-align: top;
        }

        .chatbot-launcher-inline {
          width: 45px;
          height: 45px;
          border-radius: 50%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          font-size: 18px;
          cursor: pointer;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          margin-left: 10px;
        }

        .chatbot-launcher-inline:hover {
          transform: scale(1.1);
          box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }

        .chatbot-launcher-inline:active {
          transform: scale(0.95);
        }

        .chatbot-launcher {
          width: 70px;
          height: 70px;
          border-radius: 50%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          font-size: 28px;
          cursor: pointer;
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          animation: pulse 2s infinite, float 3s ease-in-out infinite;
        }

        .chatbot-launcher:hover {
          transform: scale(1.1) rotate(10deg);
          box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
        }

        .chatbot-launcher:active {
          transform: scale(0.95);
        }

        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
          70% { box-shadow: 0 0 0 15px rgba(102, 126, 234, 0); }
          100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
        }

        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-5px); }
          100% { transform: translateY(0px); }
        }

        .chatbot-container {
          width: 380px;
          height: 550px;
          background: linear-gradient(145deg, #ffffff, #f8f9fa);
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid rgba(255, 255, 255, 0.2);
          backdrop-filter: blur(10px);
          animation: slideUp 0.4s ease-out;
          z-index: 999999 !important; /* Ensure container is also on top */
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          margin: 0;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        .chatbot-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .chatbot-header h3 {
          margin: 0;
          font-weight: 600;
          font-size: 1.1rem;
        }

        .close-button {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          font-size: 24px;
          cursor: pointer;
          padding: 8px;
          border-radius: 50%;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s ease;
        }

        .close-button:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: rotate(90deg);
        }

        .chat-messages {
          flex: 1;
          padding: 20px;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 12px;
          background: rgba(255, 255, 255, 0.5);
        }

        .message {
          max-width: 85%;
          border-radius: 18px;
          padding: 14px 18px;
          margin: 8px 0;
          word-wrap: break-word;
          animation: fadeIn 0.3s ease-out;
          position: relative;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .user {
          align-self: flex-end;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 4px;
        }

        .assistant {
          align-self: flex-start;
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          color: #333;
          border-bottom-left-radius: 4px;
        }

        .message-content {
          font-size: 0.95rem;
          line-height: 1.4;
          margin-bottom: 4px;
        }

        .message-timestamp {
          font-size: 0.7rem;
          opacity: 0.7;
          text-align: right;
          margin-top: 4px;
        }

        .typing-message {
          padding: 12px 16px;
          display: flex;
          align-items: center;
        }

        .typing-indicator {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: #667eea;
          border-radius: 50%;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) {
          animation-delay: -0.32s;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }

        .chat-input-form {
          display: flex;
          padding: 20px;
          border-top: 1px solid rgba(0, 0, 0, 0.05);
          background: white;
          gap: 10px;
        }

        .chat-input {
          flex: 1;
          padding: 14px 20px;
          border: 2px solid #e9ecef;
          border-radius: 25px;
          outline: none;
          font-size: 0.95rem;
          transition: all 0.2s ease;
          background: #f8f9fa;
        }

        .chat-input:focus {
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
          background: white;
        }

        .send-button {
          padding: 14px 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          font-size: 1.2rem;
          transition: all 0.2s ease;
          min-width: 50px;
        }

        .send-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .send-button:disabled {
          background: #ccc;
          cursor: not-allowed;
          transform: none;
          box-shadow: none;
        }

        /* Scrollbar styling */
        .chat-messages::-webkit-scrollbar {
          width: 6px;
        }

        .chat-messages::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.05);
          border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 3px;
        }

        .chat-messages::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        /* Responsive design */
        @media (max-width: 768px) {
          .chatbot-container {
            width: 340px;
            height: 500px;
            bottom: 20px;
            right: 20px;
          }

          .chatbot-launcher {
            width: 60px;
            height: 60px;
            bottom: 20px;
            right: 20px;
          }
        }

        @media (max-width: 480px) {
          .chatbot-container {
            width: calc(100vw - 40px);
            height: 450px;
            bottom: 20px;
            right: 20px;
            left: 20px;
          }
        }
      `}</style>
    </div>
  );
};

export default ChatbotWidget;