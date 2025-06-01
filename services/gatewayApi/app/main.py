from fastapi import FastAPI
from app.api.v1.routers import api_router
from app.utilities.log import logger

app = FastAPI(    title="API Gateway",
                  version="1.0",
                  on_startup=[lambda: logger.info("Starting API Gateway")],
                  on_shutdown=[lambda: logger.info("Shutting down API Gateway")]
                  )

app.include_router(api_router)

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
