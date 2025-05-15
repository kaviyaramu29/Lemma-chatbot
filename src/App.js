import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userEntry = { sender: 'user', text: message };
    setChatHistory([...chatHistory, userEntry]);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      const botEntry = { sender: 'bot', text: data.response };
      setChatHistory(prev => [...prev, botEntry]);
    } catch (error) {
      console.error('Error sending message:', error);
    }

    setMessage('');
  };

  return (
    <div className="App">
      <h1>GemmaChat</h1>
      <div className="chat-box">
        {chatHistory.map((entry, idx) => (
          <div key={idx} className={entry.sender}>
            <strong>{entry.sender === 'user' ? 'You' : 'Bot'}:</strong> {entry.text}
          </div>
        ))}
      </div>
      <div className="input-row">
        <input
          type="text"
          value={message}
          placeholder="Type a message..."
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
