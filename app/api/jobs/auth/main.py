import os
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi import HTTPException, Security
from starlette.status import HTTP_403_FORBIDDEN

UserSession = APIKey
API_KEY = os.getenv("SERVICE_SECRET_KEY_JOBS")
API_KEY_NAME_JOBS = "x-vorian-jobs-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME_JOBS, auto_error=False)


async def validate_token(vorian_api_key: str = Security(api_key_header)):
    if vorian_api_key == API_KEY:
        return vorian_api_key
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Wrong x-vorian-jobs-key.")
