from pydantic import BaseModel
from typing import Dict, Optional


class UserData(BaseModel):
    user_data: Dict


class UserUpdate(BaseModel):
    airtableID: str


class UserUpdateEmail(BaseModel):
    email: str


class UserUpdateFloidClaveBancaria(BaseModel):
    bank: str
    status: str
    date: Optional[str]


class UserUpdateFloidClaveBancariaStatus(BaseModel):
    status: str


class UserUpdateFloidClaveUnica(BaseModel):
    date: Optional[str]
    status: str
    AFC: Dict
    CMF: Dict
    SII: Dict


class UserUpdateFloidClaveUnicaStatus(BaseModel):
    status: str


class UserUpdateCaseId(BaseModel):
    uuid: str
    case_id: str
    notification_type: str

