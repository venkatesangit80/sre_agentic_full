import React, { useEffect, useState } from 'react';
import ChatWindow from './components/ChatWindow';
import InputBox from './components/InputBox';
import LogsPanel from './components/LogsPanel';
import LoadingSpinner from './components/LoadingSpinner';
import { createSession, sendMessage } from './api';
import './App.css';

const App = () => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [logs, setLogs] = useState([]);
  const [showLogs, setShowLogs] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const startSession = async () => {
      const id = await createSession();
      setSessionId(id);
    };
    startSession();
  }, []);

  const handleSend = async () => {
    if (!userInput.trim()) return;
    const userText = userInput;
    setMessages([...messages, { sender: 'user', text: userText }]);
    setUserInput('');
    setLoading(true);

    try {
      const { response, logs } = await sendMessage(sessionId, userText);
      setMessages(prev => [...prev, { sender: 'assistant', text: response }]);
      setLogs(logs);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'assistant', text: 'Error retrieving response.' }]);
      setLogs([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h2 className="title">Agentic Chatbot</h2>
      <ChatWindow messages={messages} />
      {loading && <LoadingSpinner />}
      <InputBox userInput={userInput} setUserInput={setUserInput} onSend={handleSend} />
      <div className="logs-toggle">
        <label>
          <input type="checkbox" checked={showLogs} onChange={() => setShowLogs(!showLogs)} />
          Show Execution Trace
        </label>
      </div>
      {showLogs && logs.length > 0 && <LogsPanel logs={logs} />}
    </div>
  );
};

export default App;