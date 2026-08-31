from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import agents, auth, chat, history
from app.core.database import init_models
from app.core.logging_config import configure_logging, logger
from app.utils.tracing import configure_langsmith

configure_logging()
configure_langsmith()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting GovroPK backend...")
    try:
        await init_models()
        logger.info("Database models initialized")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"DB init failed (will retry on first request): {exc}")
    yield
    logger.info("Shutting down GovroPK backend...")


app = FastAPI(
    title="GovroPK API",
    description="Multi-agent AI platform for Pakistani citizen government services",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error on {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please try again later."},
    )


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "govropk-backend"}


app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
