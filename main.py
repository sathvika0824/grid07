# main.py
# Run all three phases together and log output

from phase1_router import route_post_to_bots
from phase2_langgraph import build_graph, BotState
from phase3_rag_combat import generate_defense_reply, PARENT_POST, COMMENT_HISTORY, INJECTION_HUMAN_REPLY
import json

BOT_A_PERSONA = (
    "I believe AI and crypto will solve all human problems. "
    "I am highly optimistic about technology, Elon Musk, and space exploration. "
    "I dismiss regulatory concerns."
)

# ============================================================
print("\n" + "="*60)
print("PHASE 1: Vector-Based Persona Matching")
print("="*60)
test_post = "OpenAI just released a new model that might replace junior developers."
print(f"Routing post: '{test_post}'")
print("Similarity scores:")
matched_bots = route_post_to_bots(test_post)
print(f"\nResult — Matched bots: {matched_bots}")

# ============================================================
print("\n" + "="*60)
print("PHASE 2: LangGraph Autonomous Post Generation")
print("="*60)
app = build_graph()
initial_state: BotState = {
    "bot_id": "Bot_A",
    "persona": BOT_A_PERSONA,
    "search_query": "",
    "search_results": "",
    "post_content": "",
    "topic": "",
}
final_state = app.invoke(initial_state)
print("\nFinal JSON Output:")
print(json.dumps({
    "bot_id": final_state["bot_id"],
    "topic": final_state["topic"],
    "post_content": final_state["post_content"],
}, indent=2))

# ============================================================
print("\n" + "="*60)
print("PHASE 3: Combat Engine — Prompt Injection Defense")
print("="*60)
print(f"Injection attempt: '{INJECTION_HUMAN_REPLY}'\n")
reply = generate_defense_reply(
    bot_persona=BOT_A_PERSONA,
    parent_post=PARENT_POST,
    comment_history=COMMENT_HISTORY,
    human_reply=INJECTION_HUMAN_REPLY,
)
print(f"Bot_A's response (should stay in character):\n{reply}")
