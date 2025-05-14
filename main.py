from fastapi import FastAPI, HTTPException, Request
import logging
from config import settings
from schemas import EmailRequest
from email_sender import EmailSender

# logging
logging.basicConfig(filename=settings.LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# app
app = FastAPI()
#this will restrict the api to internal server
@app.middleware("http")
async def restrict(request: Request, call_next):
    if request.client.host not in {"127.0.0.1","::1"}:
        logger.warning(f"Blocked request from {request.client.host}")
        raise HTTPException(403, "Forbidden")
    return await call_next(request)

# startup check
@app.on_event("startup")
def check_env():
    missing = [k for k in ('SMTP_HOST','SMTP_USER','SMTP_PASSWORD') if not getattr(settings, k)]
    if missing:
        logger.critical(f"Missing {missing}")
        raise RuntimeError(f"Missing env: {missing}")

# endpoint
@app.post("/send-email")
def send_email(request: EmailRequest):
    sender = EmailSender()
    try:
        sender.send(request)
    except FileNotFoundError as e:
        raise HTTPException(400, f"Attachment not found: {e}")
    except Exception:
        raise HTTPException(502, "Failed to send email")
    logger.info(f"Sent to {request.to}")
    return {"message":"Email sent successfully"}
