import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.logging import logging_manager

logger = logging_manager.get_logger("middleware")


class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()

        # 요청 정보 로깅
        logger.info(f"{request.method} {request.url.path} started")

        # 실제 API 처리
        response = await call_next(request)

        # 처리 시간 계산 및 응답 로깅
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} completed "
            f"in {process_time:.2f}s (status: {response.status_code})"
        )
        return response
