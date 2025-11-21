import os, numpy as np
# This helper tries to use OpenAI via LangChain if OPENAI_API_KEY is set.
# Otherwise it falls back to a simple deterministic embedding (hash-based) for offline use.
def get_embedding(text: str):
    text = (text or "")[:2000]
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        try:
            from langchain.embeddings import OpenAIEmbeddings
            embeds = OpenAIEmbeddings()
            return embeds.embed_documents([text])[0]
        except Exception:
            pass
    # fallback: simple hash-based pseudo-embedding
    arr = np.zeros(384, dtype=float)
    for i, ch in enumerate(text):
        arr[i % 384] += ord(ch) % 31
    # normalize
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr.tolist()
    return (arr / norm).tolist()

def cosine_similarity(a, b):
    a = np.array(a); b = np.array(b)
    if a.size == 0 or b.size == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
