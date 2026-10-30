# 🤖 Enterprise Support & Logistics AI Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.32%2B-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/LangGraph-Workflow-orange.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/Groq-Qwen%20Model-green.svg" alt="Groq API">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Tests-Pytest-yellowgreen.svg" alt="Tests">
</p>

An advanced, secure, and production-ready enterprise AI agent built using **LangGraph**, **Streamlit**, and **Groq**. It features automated custom tool-calling for shipping cost calculations and inventory lookups, supported by robust error handling, self-correction loops, persistent multi-turn conversational memory, and full unit test coverage.

---

## 🏗️ Detailed System Architecture & Workflow

The agent follows an iterative decision-making and tool-execution loop powered by LangGraph:

```text
User Request 
     │
     ▼
Agent Decision (LLM Engine) 
     │
     ├─► [Tool Required?] ──► Custom Tool Registry (Shipping / Inventory)
     │                              │
     │                              ▼
     │                     Try/Except Guardrail
     │                              │
     │                 ┌────────────┴────────────┐
     │           [Success]                   [Error/Invalid]
     │               │                           │
     │               ▼                           ▼
     │       Return Tool Output          Self-Correction Loop 
     │               │                   (Sends traceback back to LLM)
     │               └────────────┬──────────────┘
     │                            │
     └────────────────────────────┘
     │
     ▼
Final Response to User (Streamlit UI)


### 🔍 Component Breakdown:

1. **🖥️ Presentation Layer (Streamlit UI)**:
   - Provides an intuitive chat interface.
   - Manages session state, conversation visibility, and API key protection using Streamlit Secrets.

2. **🧠 Orchestration Layer (LangGraph StateGraph)**:
   - Controls the agentic execution loop using `MessagesState`.
   - Utilizes conditional routing: dynamically decides whether the agent should execute a tool call or respond directly to the user based on the LLM's reasoning.

3. **⚡ High-Speed Inference Engine (Groq + Qwen)**:
   - Powered by `qwen/qwen3.8-27b` running on Groq LPU hardware for near-instant reasoning.
   - Temperature is set to 0 for strict, deterministic outputs during tool binding and calculations.

4. **🛠️ Execution & Safety Layer (Custom Tools & Self-Correction)**:
   - **Logistics Tools**: Executes deterministic logic (`calculate_shipping_cost`) and queries state simulation (`check_inventory_database`).
   - **Error-Recovery Loop**: All tools are wrapped in `try-except` blocks. If input validation or execution fails (e.g., negative input values), a standardized `ToolMessage` containing the error is fed back into the graph, enabling the agent to reason about the failure and self-correct on the next turn.

5. **💾 State Persistence Layer (MemorySaver)**:
   - Uses `MemorySaver` checkpointing, keyed by `thread_id`, to seamlessly retain conversation context and multi-step reasoning history across user sessions.

---

## 📂 Project Directory Structure

```text
AI-Agent-with-Tool-Calling/
│
├── .streamlit/
│   └── secrets.toml          # Secure storage for API keys (git-ignored)
├── app.py                    # Main Streamlit application & LangGraph workflow logic
├── test_tools.py             # Unit tests for custom logistics tools (pytest)
├── requirements.txt          # Project python dependencies
├── .gitignore                # Files to ignore (secrets, caches)
├── architecture_light.png    # System Architecture Diagram (Light Mode)
├── architecture_dark.png     # System Architecture Diagram (Dark Mode)
└── README.md                 # Project documentation

## ⚙️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/bhardwajarpit888-hash/AI-Agent-with-Tool-Calling.git
   cd AI-Agent-with-Tool-Calling
