### --------- External Imports --------- ###
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

### --------- Internal Imports --------- ###
from database.database_init import init_database
from routes.history_router import history_router
from routes.healthcheck_router import healthcheck_router
from routes.sentiment_classifier_router import classify_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_database()
    yield
    print("Shutting down database...")


### --------- App --------- ###
app = FastAPI(
    title="Sentiment Analyzer API",
    description="API for sentiment analysis",
    version="1.0.0",
    lifespan=lifespan,
)


### --------- Routes --------- ###
app.include_router(healthcheck_router)
app.include_router(classify_router)
app.include_router(history_router)


### --------- Middleware --------- ###
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### --------- Main --------- ###
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
