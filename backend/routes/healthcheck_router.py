### Implementing health check route

### --------- Imports --------- ###
from fastapi import APIRouter
from fastapi.responses import JSONResponse

### --------- Routes --------- ###
healthcheck_router = APIRouter(
    prefix="/api/v1",
    tags=["Health Check"],
)


@healthcheck_router.get("/health")
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "message": "The API is up and running",
        },
    )
