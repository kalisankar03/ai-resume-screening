from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os, sqlite3
from app.services.parser import extract_text
from app.services.embeddings import get_embedding
from app.db.db import insert_candidate, get_all_embeddings, init_db
from app.services.matching import match_jd
from app.langchain_chains import generate_match_summary
from app.services.emailer import send_screening_email

router = APIRouter()
UPLOAD_DIR = os.path.abspath(os.path.join(os.getcwd(), "data", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.on_event("startup")
def startup_event():
    init_db()

@router.post("/upload_resume")
async def upload_resume(name: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    safe_name = email.replace("@","_at_")
    save_path = os.path.join(UPLOAD_DIR, f"{safe_name}_{file.filename}")
    with open(save_path, "wb") as f:
        f.write(await file.read())
    resume_text = extract_text(save_path)
    emb = get_embedding(resume_text)
    candidate_id = insert_candidate(name, email, resume_text, save_path, emb)
    return {"id": candidate_id, "message": "uploaded"}

@router.post("/match")
async def match(jd_text: str = Form(...), top_k: int = Form(5)):
    results = match_jd(jd_text, top_k)
    for r in results:
        r["summary"] = generate_match_summary(r.get("resume_text","")[:1500], jd_text[:1500], r.get("score",0.0))
    return JSONResponse(results)

@router.post("/email_candidate")
async def email_candidate(candidate_id: int = Form(...), subject: str = Form(...), body: str = Form(...)):
    conn = sqlite3.connect(os.path.abspath(os.path.join(os.getcwd(), "data", "db.sqlite3")))
    cur = conn.cursor()
    cur.execute("SELECT email FROM candidates WHERE id=?", (candidate_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="candidate not found")
    to_email = row[0]
    send_screening_email(to_email, subject, body)
    return {"message": "email sent"}
