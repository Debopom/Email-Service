# app/providers/smtp_provider.py

import smtplib
from socket import gaierror
from email.message import EmailMessage
import mimetypes
import os
import logging
from app.core.config import settings
from app.providers.base_provider import EmailProvider
from app.schemas.email_schema import EmailRequest

logger = logging.getLogger("email_service")

class SMTPProvider(EmailProvider):
    def __init__(self, config):
        self.host = config.SMTP_HOST
        self.port = config.SMTP_PORT
        self.user = config.SMTP_USER
        self.pwd = config.SMTP_PASSWORD
        self.use_tls = config.USE_TLS

    def send_email(self, req: EmailRequest) -> None:
        msg = EmailMessage()
        to_list = req.to if isinstance(req.to, list) else [req.to]
        msg["From"] = self.user
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = req.subject or ""

        # 1) Plain‐text fallback:
        #    strip tags if you like, or just give a generic message
        plain = "This email contains HTML content. Please view in an HTML‐capable client."
        msg.set_content(plain)

        # 2) HTML part:
        html = req.body or ""
        msg.add_alternative(html, subtype="html")

        # 3) Attach files if any
        for path in req.attachments or []:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"Attachment not found: {path}")
            ctype, _ = mimetypes.guess_type(path)
            maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
            with open(path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(path)
                )

        # 4) Send via SMTP
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.user, self.pwd)
                server.send_message(msg)
                logger.info(f"send_email called with to={req.to}, subject={req.subject}, template={req.template_name}")
        except gaierror as e:
            raise RuntimeError(f"DNS resolution failed: {e}")
        except smtplib.SMTPException as e:
            raise RuntimeError(f"SMTP error: {e}")
