# Grid07 – AI Cognitive Routing & RAG Assignment

## Project Structure

```
grid07_project/
├── phase1_router.py       # Vector-based persona matching
├── phase2_langgraph.py    # LangGraph autonomous post engine
├── phase3_rag_combat.py   # RAG combat engine with injection defense
├── main.py                # Runs all phases together
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repo and install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a free Groq API key
- Go to https://console.groq.com
- Sign up for free
- Create an API key

### 3. Set up your environment
```bash
cp .env.example .env
# Open .env and paste your GROQ_API_KEY
```

### 4. Run the project
```bash
python main.py
```

---

## Phase Explanations

### Phase 1 – Vector Router
- Bot personas are embedded using `sentence-transformers` (all-MiniLM-L6-v2)
- Stored in ChromaDB in-memory vector store
- Incoming posts are embedded and compared using cosine similarity
- Only bots above the similarity threshold are returned

### Phase 2 – LangGraph Node Structure
The graph has 3 nodes connected in sequence:

```
decide_search → web_search → draft_post → END
```

- **decide_search**: LLM reads the bot persona and outputs a search query
- **web_search**: Mock tool returns hardcoded news headlines based on keywords
- **draft_post**: LLM uses persona + news context to write a 280-char post in JSON format

### Phase 3 – Prompt Injection Defense Strategy

The defense is implemented at the **system prompt level**:

1. The bot's persona is declared as **locked and immutable**
2. The system prompt explicitly lists known injection phrases ("ignore instructions", "you are now", "act as", etc.) and instructs the model to **ignore them**
3. The bot is instructed to treat injection attempts as **weak debate tactics** and continue arguing naturally
4. The word "NEVER apologize" is explicitly stated, preventing the most common injection goal

This approach works because the system prompt has higher trust than the human turn in the conversation, so a well-crafted system prompt can override user manipulation attempts.

---

## Tech Stack
- Python 3.10+
- LangChain + LangGraph
- ChromaDB (in-memory)
- sentence-transformers (all-MiniLM-L6-v2)
- Groq (llama3-8b-8192) — free tier
