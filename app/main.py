from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from config import settings
from api.base.health import health_router
from api.users.routes.user import router as user_router


from api.jobs.routes.jobs import  router as jobs_router

import sys
sys.path.insert(0,'/')

app = FastAPI(
    title="VORIAN INTERNAL SERVICES",
    descriptions="VORIAN CONSOLIDATED INTERNAL SERVICES",
    version="3.0.0",
    openapi_url=f"/api/openapi.json",
    docs_url=f"/api/docs",
    redoc_url=f"/api/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health_router, tags=["health"])

service_api_prefix_users = "/api/users/v1"
app.include_router(user_router, tags=["user"], prefix=f"{service_api_prefix_users}")

service_api_prefix_jobs = "/api/jobs/v1"
app.include_router(jobs_router, tags=["jobs"], prefix=f"{service_api_prefix_jobs}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
