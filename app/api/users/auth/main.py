import os
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi import HTTPException, Security, Request, Body
import os

UserSession = APIKey
API_KEY = os.getenv("SERVICE_SECRET_KEY_USERS")
API_KEY_NAME_USERS = "vorian-user-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME_USERS, auto_error=False)


async def validate_token(vorian_api_key: str = Security(api_key_header), req: Request = Request):
    if vorian_api_key is None:
        raise HTTPException(403, detail="Permission denied.")

    if vorian_api_key != API_KEY:
        raise HTTPException(403, detail="Invalid key. Permission Denied.")

    return vorian_api_key
