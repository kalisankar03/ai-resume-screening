# AI Resume Screening - Minimal Example

Structure provides a runnable skeleton for the project:
- backend: FastAPI app with upload, matching, email endpoints
- frontend: Vite + React minimal UI
- docker-compose for local development

Steps:
1. Copy the repository.
2. Create a `.env` file with keys: OPENAI_API_KEY (optional), SMTP_* vars for emailing.
3. Run with Docker Compose: `docker-compose up --build`
4. Backend: http://localhost:8000/docs
5. Frontend: http://localhost:3000

Notes:
- The provided embedding function uses OpenAI if API key is set; otherwise it falls back to a deterministic local embedding (suitable for demo/testing).
- Do NOT commit secrets.
