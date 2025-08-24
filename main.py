from contextlib import asynccontextmanager

from fastapi import FastAPI

from chat.router import router as chat_router
from core.logging import logging_manager
from core.middleware import LoggingMiddleWare
from model.model_manager import ModelManager

logger = logging_manager.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        logger.info("Loading model...")
        app.state.modelManager = ModelManager()
        app.state.modelManager.load_model()
        logger.info("Model loaded!")

        # 여기서 로직이 실행됨
        yield
    except Exception as e:
        logger.error(f"Startup error: {e}")
    finally:
        # Shutdown logic
        del app.state.modelManager


app = FastAPI(
    title="Local LLM API Server",
    description="로컬 MLX LLM 모델을 위한 OpenAI 호환 API 서버",
    version="0.1.0",
    lifespan=lifespan,
)

# 미들웨어 등록
app.add_middleware(LoggingMiddleWare)

# 라우터 등록
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Local LLM API Server is running!"}
