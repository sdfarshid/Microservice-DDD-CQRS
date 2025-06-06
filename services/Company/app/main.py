from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.infrastructure.database.session import init_db
from app.utilities.log import logger

app = FastAPI(title="Company Service",
              version="1.0",
              debug=True,
              on_startup=[lambda: logger.info("Starting Company Service")],
              on_shutdown=[lambda: logger.info("Shutting down Company Service")]
              )


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
