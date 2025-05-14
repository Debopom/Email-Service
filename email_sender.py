import smtplib
import mimetypes
import os
import logging
from socket import gaierror
from email.message import EmailMessage
from schemas import EmailRequest
from config import settings

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.pwd = settings.SMTP_PASSWORD
        self.use_tls = settings.USE_TLS

    def send(self, req: EmailRequest):
        msg = EmailMessage()
        to_list = req.to if isinstance(req.to, list) else [req.to]
        msg["From"] = self.user
        msg["To"] = ", ".join(to_list)
        msg["Subject"] = req.subject
        subtype = "html" if "<" in req.body else "plain"
        msg.set_content(req.body, subtype=subtype)

        # attachments
        for path in req.attachments or []:
            if not os.path.isfile(path):
                raise FileNotFoundError(path)
            ctype, _ = mimetypes.guess_type(path)
            if not ctype:
                ctype = "application/octet-stream"
            maintype, sub = ctype.split("/",1)
            with open(path, "rb") as f:
                msg.add_attachment(f.read(), maintype=maintype, subtype=sub, filename=os.path.basename(path))

        try:
            with smtplib.SMTP(self.host, self.port) as s:
                if self.use_tls:
                    s.starttls()
                s.login(self.user, self.pwd)
                s.send_message(msg)
        except gaierror:
            logger.error(f"Cannot resolve SMTP host {self.host}")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            raise