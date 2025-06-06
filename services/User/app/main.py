

from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.infrastructure.database.session import init_db
from app.utilities.log import logger

app = FastAPI(    title="User Service",
                  version="1.0",
                  on_startup=[lambda: logger.info("Starting User Service")],
                  on_shutdown=[lambda: logger.info("Shutting down User Service")]
                  )

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    print(" Running database initialization...")
    await init_db()





@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
