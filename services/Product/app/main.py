from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.infrastructure.database.session import init_db
from app.utilities.log import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Product Service")
    print("Starting database initialization...")
    await init_db()
    print("Database initialized!")

    yield

    logger.info("Shutting down Product Service")



app = FastAPI(title="Product Service",
              version="1.0",
              debug=True,
              on_startup=[lambda: logger.info("Starting Product Service")],
              on_shutdown=[lambda: logger.info("Shutting down Product Service")]
              )

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
