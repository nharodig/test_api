from fastapi import APIRouter, Request, HTTPException, Depends

from ..jobs.routes.health import health_check as jobs_health_check

from ..users.routes.health import health_check as users_health_check

from ..jobs.database.conf import db_jobs

from ..users.database.conf import db_users



import logging

health_router = APIRouter()


@health_router.get("/health", response_description="Health endpoint", summary="health")
async def health_check(
        db_jobs=Depends(db_jobs),
        db_users=Depends(db_users)
):
    try:

        jobs_health_check(db_jobs)
        users_health_check(db_users)


    except Exception as e:
        logging.error(type(e))    # the exception type
        logging.error(e.args)     # arguments stored in .args
        logging.error(e)
        raise HTTPException(status_code=500, detail="errorDetail")
    else:
        return {"status": 200, "message": "Server Alive!"}
