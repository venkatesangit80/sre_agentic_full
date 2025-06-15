const API_URL = "http://localhost:8000"; // Adjust if backend is hosted elsewhere

export const createSession = async () => {
  const res = await fetch(`${API_URL}/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  const data = await res.json();
  return data.sessionId;
};

export const sendMessage = async (sessionId, message) => {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sessionId, message }),
  });
  const data = await res.json();
  return data;
};