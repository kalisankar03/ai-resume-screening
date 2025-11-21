from app.services.embeddings import get_embedding, cosine_similarity
from app.db.db import get_all_embeddings
def match_jd(jd_text: str, top_k: int = 5):
    jd_emb = get_embedding(jd_text)
    candidates = get_all_embeddings()
    scored = []
    for c in candidates:
        if not c.get('embedding'): continue
        score = cosine_similarity(jd_emb, c['embedding'])
        scored.append({**c, "score": score})
    scored = sorted(scored, key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
