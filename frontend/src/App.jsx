import { useState, useRef, useEffect } from 'react';
import './index.css';

const BACKEND_URL = 'http://localhost:5000';

// Generate a random session ID once per browser tab, so conversations
// can be grouped without needing user accounts or personal info.
function generateSessionId() {
  return 'session-' + Math.random().toString(36).substring(2, 15) + Date.now();
}

function App() {
  const [sessionId] = useState(generateSessionId);
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Hi, I'm here to listen. How are you feeling today?",
      technique: null,
    },
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

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage = { sender: 'user', text: trimmed, technique: null };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: trimmed, sessionId }),
      });

      if (!res.ok) throw new Error('Server error');

      const data = await res.json();

      const botMessage = {
        sender: 'bot',
        text: data.reply,
        technique: data.technique,
        isCrisis: data.is_crisis,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: "I'm having trouble connecting right now. Please try again in a moment.",
          technique: null,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>MindSpace</h1>
        <p className="disclaimer">
          This is a supportive tool, not a replacement for professional care.
          If you're in crisis, please contact a crisis line immediately.
        </p>
      </header>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender} ${msg.isCrisis ? 'crisis' : ''}`}>
            <div className="bubble">
              <p>{msg.text}</p>
              {msg.technique && (
                <div className="technique-card">
                  <strong>{msg.technique.name}</strong>
                  <p className="technique-desc">{msg.technique.description}</p>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="bubble typing">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-bar">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type how you're feeling..."
          rows={1}
        />
        <button onClick={sendMessage} disabled={isLoading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;