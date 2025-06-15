import React from 'react';
import './LogsPanel.css';

const LogsPanel = ({ logs }) => {
  return (
    <div className="logs-panel">
      <h4>Execution Trace</h4>
      <ul>
        {logs.map((log, index) => (
          <li key={index}>{log}</li>
        ))}
      </ul>
    </div>
  );
};

export default LogsPanel;