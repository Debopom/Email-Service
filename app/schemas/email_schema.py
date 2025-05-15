from pydantic import BaseModel, EmailStr
from typing import List, Union, Optional, Dict, Any

class EmailRequest(BaseModel):
    to: Union[EmailStr, List[EmailStr]]
    subject: Optional[str] = None
    body:    Optional[str] = None
    template_name:    Optional[str] = None  # e.g. "example_email.html"
    template_data:    Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None

class EmailResponse(BaseModel):
    message: str
