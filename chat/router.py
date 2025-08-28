from typing import Optional

from fastapi import APIRouter, Request

from chat.models import ChatCompletionRequest, ChatCompletionResponse
from chat.service import process_chat_completion

router = APIRouter(
    prefix="/v1",  # 모든 엔드포인트에 /v1 접두사
    tags=["chat"],  # Swagger 문서에서 그루핑
)


@router.post("/chat/completions")
async def chat_completions(
    request: Request,
    chatCompletionRequest: ChatCompletionRequest,
) -> Optional[ChatCompletionResponse]:

    modelManager = request.app.state.modelManager

    return process_chat_completion(model_manager=modelManager, chat_completion_request=chatCompletionRequest)
