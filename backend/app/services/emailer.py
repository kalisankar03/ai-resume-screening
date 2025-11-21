import smtplib, os
from email.message import EmailMessage

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL")

def send_screening_email(to_email: str, subject: str, body: str):
    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD or not FROM_EMAIL:
        raise RuntimeError("SMTP not configured. Set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD and FROM_EMAIL.")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USERNAME, SMTP_PASSWORD)
        s.send_message(msg)
