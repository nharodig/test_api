from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text




# @healthRouter.get("/health", response_description="Health endpoint", summary="health")
# async def health_check(DB=Depends(db)):
def health_check(DB:Session):
    try:
        DB.execute(text("SELECT 1"))
    except:
        raise HTTPException(status_code=500, detail="errorDetail")
    else:
        return {"status": 200, "message": "Server Alive!"}
