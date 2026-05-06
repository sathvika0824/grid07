# phase2_langgraph.py
# Phase 2: The Autonomous Content Engine using LangGraph
#
# Flow:
#   Node 1 (decide_search) → Node 2 (web_search) → Node 3 (draft_post) → END
#
# Each node receives the shared "state" dict and returns updated fields.

import os
import json
from dotenv import load_dotenv
from typing import TypedDict

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

load_dotenv()

# ---------------------------------------------------------------------------
# 1. Define the shared state that flows through the graph
# ---------------------------------------------------------------------------
class BotState(TypedDict):
    bot_id: str
    persona: str
    search_query: str       # filled by Node 1
    search_results: str     # filled by Node 2
    post_content: str       # filled by Node 3
    topic: str              # filled by Node 3


# ---------------------------------------------------------------------------
# 2. Mock search tool — returns fake but realistic headlines
# ---------------------------------------------------------------------------
@tool
def mock_searxng_search(query: str) -> str:
    """Simulates a web search and returns hardcoded news headlines."""
    query_lower = query.lower()

    if "crypto" in query_lower or "bitcoin" in query_lower:
        return "Bitcoin hits new all-time high amid regulatory ETF approvals. Ethereum sees 40% surge."

    if "ai" in query_lower or "openai" in query_lower or "llm" in query_lower:
        return "OpenAI launches GPT-5 with real-time reasoning. Google DeepMind responds with Gemini Ultra 2."

    if "stock" in query_lower or "market" in query_lower or "rate" in query_lower:
        return "Fed holds interest rates steady at 5.25%. S&P 500 gains 1.2% on strong earnings reports."

    if "elon" in query_lower or "tesla" in query_lower or "space" in query_lower:
        return "SpaceX Starship completes first successful Mars trajectory test. Tesla FSD 13 released."

    if "regulation" in query_lower or "privacy" in query_lower:
        return "EU passes sweeping AI regulation bill. Big Tech faces record fines for data misuse."

    return "Tech sector sees mixed results as global markets remain volatile."


# ---------------------------------------------------------------------------
# 3. LLM setup (using Groq — free tier available at console.groq.com)
# ---------------------------------------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
)


# ---------------------------------------------------------------------------
# 4. Node 1 — Decide what to search for
# ---------------------------------------------------------------------------
def decide_search(state: BotState) -> BotState:
    """LLM reads the bot persona and decides what topic to post about today."""
    messages = [
        SystemMessage(content=f"You are: {state['persona']}"),
        HumanMessage(content=(
            "You want to make a post today. "
            "Decide ONE topic you care about and write a short search query (5 words max). "
            "Reply with ONLY the search query, nothing else."
        )),
    ]
    response = llm.invoke(messages)
    state["search_query"] = response.content.strip()
    print(f"[Node 1] Search query decided: {state['search_query']}")
    return state


# ---------------------------------------------------------------------------
# 5. Node 2 — Execute the mock web search
# ---------------------------------------------------------------------------
def web_search(state: BotState) -> BotState:
    """Runs the mock search tool using the query from Node 1."""
    results = mock_searxng_search.invoke({"query": state["search_query"]})
    state["search_results"] = results
    print(f"[Node 2] Search results: {state['search_results']}")
    return state


# ---------------------------------------------------------------------------
# 6. Node 3 — Draft the post as strict JSON
# ---------------------------------------------------------------------------
def draft_post(state: BotState) -> BotState:
    """LLM uses the persona + search results to write a 280-char post."""
    messages = [
        SystemMessage(content=f"You are: {state['persona']}"),
        HumanMessage(content=(
            f"Today's news context: {state['search_results']}\n\n"
            "Write a highly opinionated social media post (max 280 characters) based on this news.\n"
            "Reply ONLY with a valid JSON object in this exact format, no extra text:\n"
            '{"bot_id": "' + state["bot_id"] + '", "topic": "<topic>", "post_content": "<your post>"}'
        )),
    ]
    response = llm.invoke(messages)
    raw = response.content.strip()

    # Clean up in case LLM wraps in markdown code fences
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw)
        state["topic"] = parsed.get("topic", "unknown")
        state["post_content"] = parsed.get("post_content", raw)
        print(f"[Node 3] Post drafted successfully.")
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        state["topic"] = state["search_query"]
        state["post_content"] = raw[:280]
        print(f"[Node 3] Warning: Could not parse JSON. Using raw output.")

    return state


# ---------------------------------------------------------------------------
# 7. Build the LangGraph state machine
# ---------------------------------------------------------------------------
def build_graph():
    graph = StateGraph(BotState)

    graph.add_node("decide_search", decide_search)
    graph.add_node("web_search", web_search)
    graph.add_node("draft_post", draft_post)

    # Connect nodes in sequence
    graph.set_entry_point("decide_search")
    graph.add_edge("decide_search", "web_search")
    graph.add_edge("web_search", "draft_post")
    graph.add_edge("draft_post", END)

    return graph.compile()


# ---------------------------------------------------------------------------
# 8. Test it
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = build_graph()

    # Test with Bot A (Tech Maximalist)
    initial_state: BotState = {
        "bot_id": "Bot_A",
        "persona": (
            "I believe AI and crypto will solve all human problems. "
            "I am highly optimistic about technology, Elon Musk, and space exploration. "
            "I dismiss regulatory concerns."
        ),
        "search_query": "",
        "search_results": "",
        "post_content": "",
        "topic": "",
    }

    print("=== Running LangGraph for Bot_A ===\n")
    final_state = app.invoke(initial_state)

    print("\n=== Final Output ===")
    print(json.dumps({
        "bot_id": final_state["bot_id"],
        "topic": final_state["topic"],
        "post_content": final_state["post_content"],
    }, indent=2))
