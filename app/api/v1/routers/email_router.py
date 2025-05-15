from fastapi import APIRouter, Depends, HTTPException
from app.schemas.email_schema import EmailRequest, EmailResponse
from app.services.email_service import EmailService
from app.providers.smtp_provider import SMTPProvider
from app.core.config import settings

router = APIRouter()

def get_email_service():
    provider = SMTPProvider(settings)
    return EmailService(provider)

@router.post("/send", response_model=EmailResponse)
async def send_email(req: EmailRequest, service: EmailService = Depends(get_email_service)):
    try:

        service.send(req)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
