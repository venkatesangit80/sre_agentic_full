const API_URL = "http://localhost:8000"; // Adjust if backend is hosted elsewhere

export const createSession = async () => {
  const res = await fetch(`${API_URL}/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const data = await res.json();
  return data.sessionId;
};

export const sendMessage = async (sessionId, message, history = []) => {
  const res = await fetch(`${API_URL}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt: message,
      history,
      thread_id: sessionId
    }),
  });
  const data = await res.json();
  return data;
};