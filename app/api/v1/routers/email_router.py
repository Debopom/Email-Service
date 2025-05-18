from fastapi import APIRouter, HTTPException
import logging
from app.schemas.email_schema import EmailRequest, EmailResponse
from app.tasks.email_tasks import send_email_task

router = APIRouter()
logger = logging.getLogger("email_service")

@router.post("/send", response_model=EmailResponse)
async def send_email(req: EmailRequest):
    """
    Enqueue email sending as a background task.
    """
    logger.info(f"send_email called with to={req.to}, subject={req.subject}, template={req.template_name}")
    try:
        send_email_task.delay(req.dict())
        logger.info(f"Email queued for sending to {req.to}")
        return {"message": "Email queued for sending"}
    except Exception as e:
        logger.exception(f"Error queuing email to {req.to}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
