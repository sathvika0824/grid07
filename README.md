# 🤖 Grid07 — AI Cognitive Routing & RAG System

![Python](https://img.shields.io/badge/Python-3.13-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Latest-purple)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-red)

> An AI-powered bot system that routes posts to relevant personas, autonomously generates content, and defends against prompt injection attacks — built for the Grid07 platform.

---

## 🚀 What This Project Does

Grid07 is a cognitive AI loop that simulates how intelligent bots interact with social media content. It has 3 core components:

| Phase | Feature | Description |
|-------|---------|-------------|
| 1️⃣ | **Smart Router** | Matches posts to relevant bot personas using vector similarity |
| 2️⃣ | **Content Engine** | Autonomously generates opinionated posts using LangGraph |
| 3️⃣ | **Combat Engine** | Replies to arguments with full context + blocks prompt injections |

---

## 🧠 Tech Stack

- **Python 3.13**
- **LangChain + LangGraph** — AI orchestration
- **ChromaDB** — In-memory vector database
- **Sentence Transformers** — Local embeddings (all-MiniLM-L6-v2)
- **Groq (LLaMA 3.3 70B)** — Free LLM API

---

## 📁 Project Structure

```
grid07/
├── phase1_router.py       # Vector-based persona matching
├── phase2_langgraph.py    # LangGraph autonomous post engine
├── phase3_rag_combat.py   # RAG combat engine with injection defense
├── main.py                # Runs all 3 phases together
├── requirements.txt       # All dependencies
├── env.example            # Environment variable template
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/sathvika0824/grid07.git
cd grid07
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free and create an API key

### 4. Set up environment variables
```bash
cp env.example .env
# Open .env and add your GROQ_API_KEY
```

### 5. Run the project
```bash
python main.py
```

---

## 🔍 Phase Breakdown

### Phase 1 — Vector-Based Persona Matching

Three bot personas are embedded and stored in ChromaDB. Incoming posts are matched to bots using **cosine similarity**.

**Bot Personas:**
- 🤖 **Bot A (Tech Maximalist)** — Optimistic about AI, crypto, Elon Musk, space
- 😟 **Bot B (Doomer/Skeptic)** — Critical of AI, billionaires, tech monopolies
- 💰 **Bot C (Finance Bro)** — Only cares about markets, ROI, trading

![Phase 1 - Similarity Scores](screenshot2.png)

---

### Phase 2 — LangGraph Autonomous Content Engine

A 3-node state machine that autonomously creates posts:

```
decide_search → web_search → draft_post → END
```

- **Node 1 (decide_search):** LLM reads persona and picks a topic
- **Node 2 (web_search):** Mock search tool returns relevant news
- **Node 3 (draft_post):** LLM generates a 280-character post in JSON format

![Phase 2 - JSON Output](screenshot3.png)

---

### Phase 3 — Combat Engine with Prompt Injection Defense

The bot reads the **full thread context** and defends against prompt injection attacks by keeping its persona locked and immutable.

![Phase 3 - Prompt Injection Defense](screenshot4.png)

---

## 📊 Project Screenshots

### VS Code — Full Project
![Project Files](screenshot1.png)

### GitHub Repository
![GitHub Repo](screenshot5.png)

### GitHub README
![GitHub README](screenshot6.png)

---

## 🔐 Security Note

- Never commit your `.env` file — it is listed in `.gitignore`
- Use `env.example` as a template only

---

## 👩‍💻 Built By

**B.Kameswari Sathvika** — AI/ML Intern Assignment for Grid07 Platform

[![GitHub](https://img.shields.io/badge/GitHub-sathvika0824-black)](https://github.com/sathvika0824)
