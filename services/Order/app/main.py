from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.infrastructure.database.session import init_db, drop_all_tables
from app.utilities.log import logger

app = FastAPI(title="Order Service",
              version="1.0",
              debug=True,
              on_startup=[lambda: logger.info("Starting Order Service")],
              on_shutdown=[lambda: logger.info("Shutting down Order Service")]
              )


app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():

    print("Starting database initialization...")
    await init_db()
    print("Database initialized!")


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
