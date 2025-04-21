from typing import Union, Optional
from pydantic import BaseModel, Field


class UserBody(BaseModel):
    name: Optional[str]
    airtableID: Optional[str]
    email: str
    user_data: Optional[dict]
