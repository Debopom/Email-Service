from abc import ABC, abstractmethod
from app.schemas.email_schema import EmailRequest

class EmailProvider(ABC):
    @abstractmethod
    def send_email(self, req: EmailRequest) -> None:
        pass
