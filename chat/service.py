import time
import uuid

from fastapi import HTTPException
from ollama import GenerateResponse

from chat.models import ChatCompletionRequest, ChatCompletionResponse, Choice, Message, Usage
from model.model_manager import ModelManager
from templates.service import get_chat_template

def process_chat_completion(model_manager: ModelManager, chat_completion_request: ChatCompletionRequest) -> ChatCompletionResponse:
    try:
            
        # Strategy + Factory Pattern 방식
        template = get_chat_template(chat_completion_request.model)
        prompt = template.convert_messages(chat_completion_request.messages)

        result = model_manager.generate(prompt, chat_completion_request.thinking, num_predict=chat_completion_request.num_predict, repeat_penalty=chat_completion_request.repeat_penalty, top_k=chat_completion_request.top_k, top_p=chat_completion_request.top_p)

        if result is None:
            raise HTTPException(status_code=500, detail="Failed to generate response")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return convert_result_to_response(model=chat_completion_request.model, result=result)

def create_choice(response_text: str) -> Choice:
    return Choice(
        index=0,
        message=Message(role="assistant", content=response_text),
        finish_reason="stop",
    )

def calculate_usage(result: GenerateResponse) -> Usage:
    prompt_tokens = getattr(result, 'prompt_eval_count', 0) or 0
    completion_tokens = getattr(result, 'eval_count', 0) or 0
    total_tokens = prompt_tokens + completion_tokens

    return Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )


def convert_result_to_response(
    model: str, result: GenerateResponse
) -> ChatCompletionResponse:
    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:10]}",
        object="chat.completion",
        created=int(time.time()),
        model=model,
        choices=[create_choice(response_text=result.response)],
        usage=calculate_usage(result=result),
    )
