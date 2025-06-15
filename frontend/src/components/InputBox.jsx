import React from 'react';
import './InputBox.css';

const InputBox = ({ userInput, setUserInput, onSend }) => {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="input-box">
      <textarea
        className="text-input"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message..."
        rows={2}
      />
      <button className="send-button" onClick={onSend}>
        Send
      </button>
    </div>
  );
};

export default InputBox;