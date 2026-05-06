# phase1_router.py
# Phase 1: Vector-Based Persona Matching
# This module creates bot personas, stores them in a vector database,
# and routes incoming posts to the most relevant bots using cosine similarity.

from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

# ---------------------------------------------------------------------------
# 1. Define the three bot personas
# ---------------------------------------------------------------------------
BOT_PERSONAS = {
    "Bot_A": (
        "I believe AI and crypto will solve all human problems. "
        "I am highly optimistic about technology, Elon Musk, and space exploration. "
        "I dismiss regulatory concerns."
    ),
    "Bot_B": (
        "I believe late-stage capitalism and tech monopolies are destroying society. "
        "I am highly critical of AI, social media, and billionaires. "
        "I value privacy and nature."
    ),
    "Bot_C": (
        "I strictly care about markets, interest rates, trading algorithms, and making money. "
        "I speak in finance jargon and view everything through the lens of ROI."
    ),
}

# ---------------------------------------------------------------------------
# 2. Load a local embedding model (no API key needed)
# ---------------------------------------------------------------------------
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------------------------------------------------------
# 3. Set up ChromaDB in-memory vector store
# ---------------------------------------------------------------------------
chroma_client = chromadb.Client()  # in-memory, no disk needed
collection = chroma_client.create_collection(name="bot_personas")

# Embed each persona and store in ChromaDB
for bot_id, persona_text in BOT_PERSONAS.items():
    embedding = embedder.encode(persona_text).tolist()
    collection.add(
        ids=[bot_id],
        embeddings=[embedding],
        documents=[persona_text],
    )

print("Bot personas stored in vector database.\n")


# ---------------------------------------------------------------------------
# 4. Cosine similarity helper
# ---------------------------------------------------------------------------
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


# ---------------------------------------------------------------------------
# 5. Main routing function
# ---------------------------------------------------------------------------
def route_post_to_bots(post_content: str, threshold: float = 0.3):
    """
    Given a post, find which bots would 'care' about it.
    Returns a list of (bot_id, similarity_score) tuples above the threshold.

    Note: all-MiniLM-L6-v2 produces lower similarity scores than OpenAI embeddings,
    so we use a lower threshold (0.3) for realistic results.
    """
    # Embed the incoming post
    post_embedding = embedder.encode(post_content).tolist()

    # Query all bot personas from ChromaDB
    results = collection.query(
        query_embeddings=[post_embedding],
        n_results=len(BOT_PERSONAS),  # get all bots
        include=["embeddings", "documents"],
    )

    matched_bots = []
    for bot_id, persona_embedding in zip(
        results["ids"][0], results["embeddings"][0]
    ):
        score = cosine_similarity(post_embedding, persona_embedding)
        print(f"  {bot_id} similarity: {score:.4f}")
        if score >= threshold:
            matched_bots.append((bot_id, round(score, 4)))

    return matched_bots


# ---------------------------------------------------------------------------
# 6. Test it
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_post = "OpenAI just released a new model that might replace junior developers."
    print(f"Post: '{test_post}'")
    print("Similarity scores:")
    matched = route_post_to_bots(test_post)
    print(f"\nMatched bots: {matched}")
