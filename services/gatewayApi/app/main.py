from fastapi import FastAPI, Request, HTTPException
from app.api.v1.routers import api_router
from app.utilities.log import logger, DebugError
from fastapi.responses import JSONResponse

app = FastAPI(title="API Gateway",
              version="1.0",
              on_startup=[lambda: logger.info("Starting API Gateway")],
              on_shutdown=[lambda: logger.info("Shutting down API Gateway")]
              )

app.include_router(api_router)


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException):
    DebugError(f"{request.method} {request.url} -> {exc.status_code}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello World Farshid"}
