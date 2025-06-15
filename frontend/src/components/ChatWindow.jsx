import React from 'react';
import './ChatWindow.css';

const ChatWindow = ({ messages }) => {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`message ${msg.sender === 'user' ? 'user-msg' : 'bot-msg'}`}
        >
          <div className="bubble">{msg.text}</div>
        </div>
      ))}
    </div>
  );
};

export default ChatWindow;