from pydantic import BaseModel, EmailStr
from typing import List, Union, Optional

class EmailRequest(BaseModel):
    to: Union[EmailStr, List[EmailStr]]
    subject: str
    body: str
    attachments: Optional[List[str]] = None