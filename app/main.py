import os
import logging
from fastapi import FastAPI, Request, HTTPException
from app.api.v1.routers.email_router import router as email_router
from app.core.config import settings

# Determine log file path, falling back if not set in settings
default_log = "email_service.log"
log_file = getattr(settings, "LOG_FILE", default_log)
log_path = os.path.abspath(log_file)
log_dir = os.path.dirname(log_path)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
# Ensure the log file exists
open(log_path, 'a').close()

# Configure logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("email_service")

app = FastAPI(title="Email Sending Service")

@app.on_event("startup")
async def on_startup():
    logger.info("Service started and ready to send emails.")

@app.middleware("http")
async def restrict_internal(request: Request, call_next):
    client_ip = request.client.host
    if client_ip not in ("127.0.0.1", "::1"):
        logger.warning(f"Blocked unauthorized request from {client_ip}")
        raise HTTPException(status_code=403, detail="Forbidden")
    return await call_next(request)

# Include the email router under /api/v1/send
app.include_router(email_router, prefix="/api/v1")
