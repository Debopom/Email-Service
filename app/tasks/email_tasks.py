# app/tasks/email_tasks.py
from celery.utils.log import get_task_logger
from app.schemas.email_schema import EmailRequest
from app.providers.smtp_provider import SMTPProvider
from app.core.config import settings
from app.core.celery import celery_app

logger = get_task_logger(__name__)

@celery_app.task(name="send_email_task", bind=True, acks_late=True)
def send_email_task(self, data: dict) -> None:
    req = EmailRequest(**data)
    provider = SMTPProvider(settings)
    provider.send_email(req)
    msg = f"Async email sent to {req.to} with subject '{req.subject}'"
    logger.info(msg)
    print(msg)
