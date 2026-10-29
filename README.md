# 🤖 Enterprise Support & Logistics AI Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Streamlit-1.32%2B-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/LangGraph-Workflow-orange.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/Groq-Qwen%20Model-green.svg" alt="Groq API">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

An advanced, secure, and production-ready enterprise AI agent built using **LangGraph**, **Streamlit**, and **Groq**. It features automated custom tool-calling for shipping cost calculations and inventory lookups, supported by robust error handling, self-correction loops, and persistent multi-turn conversational memory.

---

## 🏗️ Architecture & Workflow Flowchart

The agent operates on an iterative decision-making loop powered by LangGraph:

```text
User Request ──► Agent Decision (LLM) ──► Tool Execution ──► Self-Correction / Response

## ⚙️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/bhardwajarpit888-hash/AI-Agent-with-Tool-Calling.git
   cd AI-Agent-with-Tool-Calling
