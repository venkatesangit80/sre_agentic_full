# 🧠 Agentic Chatbot System (Gemini + FastAPI + React)

A fully modular, dynamic, memory-backed agentic chatbot using:
- ✨ Gemini (Google Generative AI)
- ⚙️ FastAPI for backend orchestration
- 💬 React frontend for chat interface
- 🧠 ChromaDB for long-term memory & time travel
- 🔄 Agent Contracts for flexible, multi-agent logic

---

## 🚀 Features

- 🔗 **LLM-Based Planner**: Gemini dynamically decides which agents to run
- 🧱 **Structured Agent Contracts**: Each agent includes input/output instructions and execution type (`independent` or `dependent`)
- 🔍 **LLM Summary Generator**: After execution, Gemini summarizes the trace in user-friendly language
- 🧠 **ChromaDB Memory**: Stores query history with metadata for recall and time-travel debugging
- ✅ **Session-Based Memory**: Full conversation history per session
- 🧑‍⚖️ **Human-in-the-Loop Ready**: Plan approval + command interrupt design supported
- 🔁 **Follow-Up Prompts**: Planner uses full chat history for reasoning

---

## 🧰 Setup Instructions

### 1. Backend (FastAPI + ChromaDB + Gemini)

#### 🐍 Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 🌐 Set up your `.env` file
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

#### 🚀 Run FastAPI server
```bash
uvicorn main:app --reload
```
Server will start on `http://localhost:8000`

---

### 2. Frontend (React Chat Interface)

#### ⚙️ Install dependencies
```bash
cd frontend
npm install
```

#### ▶️ Start the React app
```bash
npm start
```
UI will run at `http://localhost:3000`

---

## 🧠 Architecture Overview

```text
User → React UI → FastAPI → Gemini Planner → Agent Chain
                                ↓
                          LLM Summary
                                ↓
                       Memory Store (ChromaDB)
```

### 🧱 Backend Modules
| Module           | Purpose                                       |
|------------------|-----------------------------------------------|
| `main.py`        | FastAPI entrypoint + endpoints                |
| `agent_planner.py` | Uses Gemini to generate agent plan          |
| `agent_executor.py` | Executes each agent based on plan           |
| `agent_contract.py` | Defines structure of each agent contract    |
| `agent_pipeline.py` | Runs plan + returns summary + logs          |
| `memory_store.py` | Uses ChromaDB to store + search past memory  |
| `session_store.py` | Tracks session-specific history              |

### 💡 Key Concepts

- **AgentContract**:
```json
{
  "agent": "forecast",
  "input_value": "output from health",
  "input_instruction": "Forecast CPU trend for overloaded servers",
  "output_instruction": "Detect breach in next 30 minutes",
  "action_type": "dependent"
}
```

- **Logs Example**:
```
User query: Check health of APP1
Agent plan: ['health', 'forecast']
LLM-based summary: The system checked...
Agents executed: health (independent), forecast (dependent)
```

---

## 🔬 Memory Features

- Stores agent outputs, session ID, timestamp, agents used
- Searchable using `search_memory("cpu")`
- Supports retrieval by:
  - Keywords
  - Time window
  - Agent used (e.g. `anomaly`)

---

## 📦 Project Structure

```
agentic-chatbot/
├── backend/
│   ├── main.py
│   ├── agent_contract.py
│   ├── agent_planner.py
│   ├── agent_executor.py
│   ├── agent_pipeline.py
│   ├── memory_store.py
│   ├── session_store.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/components/
│   │   ├── ChatWindow.jsx
│   │   ├── InputBox.jsx
│   │   ├── LogsPanel.jsx
│   │   └── LoadingSpinner.jsx
│   ├── App.jsx
│   ├── api.js
│   └── index.js
│
└── .env
```

---

## 💬 Example Prompts to Test

| Prompt                                               | Expected Agents             |
|------------------------------------------------------|-----------------------------|
| "Check the health of APP1"                           | `['health']`                |
| "Only forecast if health check fails"               | `['health', 'forecast']`    |
| "Detect anomalies in the system"                    | `['anomaly']`               |
| "What should we do next?" (after health)            | `['forecast']`              |
| "Tell me a joke."                                    | `[]` + gentle fallback      |

---

## ✅ To Do Next (if needed)
- Add WebSocket for streaming response/logs
- UI for editing agent plan before execution (HITL)
- Visual memory timeline (like time-travel console)
- LangGraph optional backend for visual execution tracing

---

## 🔐 Credits
Built by you — combining dynamic LLM planning with real-world infra logic. ✨