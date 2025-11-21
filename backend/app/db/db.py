import sqlite3, json, os
DB_PATH = os.path.abspath(os.path.join(os.getcwd(), "data", "db.sqlite3"))
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        resume_text TEXT,
        resume_file TEXT,
        embedding TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

def insert_candidate(name, email, resume_text, resume_file, embedding):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""INSERT INTO candidates (name, email, resume_text, resume_file, embedding) VALUES (?, ?, ?, ?, ?)""",
                (name, email, resume_text, resume_file, json.dumps(embedding)))
    conn.commit()
    candidate_id = cur.lastrowid
    conn.close()
    return candidate_id

def get_all_embeddings():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, resume_text, embedding FROM candidates")
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        emb = json.loads(r[4]) if r[4] else None
        results.append({"id": r[0], "name": r[1], "email": r[2], "resume_text": r[3], "embedding": emb})
    return results
