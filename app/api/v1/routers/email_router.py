from fastapi import APIRouter, Depends, HTTPException
import logging
from app.schemas.email_schema import EmailRequest, EmailResponse
from app.services.email_service import EmailService
from app.providers.smtp_provider import SMTPProvider
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger("email_service")

def get_email_service():
    provider = SMTPProvider(settings)
    return EmailService(provider)

@router.post("/send", response_model=EmailResponse)
async def send_email(
    req: EmailRequest,
    service: EmailService = Depends(get_email_service),
):
    logger.info(f"send_email called with to={req.to}, subject={req.subject}, template={req.template_name}")
    try:
        service.send(req)
        logger.info(f"Email successfully sent to {req.to}")
        return {"message": "Email sent successfully"}
    except Exception as e:
        logger.exception(f"Error sending email to {req.to}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
