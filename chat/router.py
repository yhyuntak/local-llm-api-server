from typing import Optional

from fastapi import APIRouter, Request
from mlx_lm import generate

from chat.models import ChatCompletionRequest, ChatCompletionResponse
from chat.service import convert_result_to_response
from templates.service import get_chat_template

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

    # Strategy + Factory Pattern 방식
    template = get_chat_template(chatCompletionRequest.model)
    prompt = template.convert_messages(chatCompletionRequest.messages)

    result = generate(
        modelManager.model,
        modelManager.tokenizer,
        prompt=prompt,
        verbose=True,
        max_tokens=chatCompletionRequest.max_tokens,
    )
    return convert_result_to_response(
        model=chatCompletionRequest.model,
        prompt=prompt,
        result=result,
        tokenizer=modelManager.tokenizer,
    )
