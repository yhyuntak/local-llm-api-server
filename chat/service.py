import time
import uuid

from chat.models import ChatCompletionResponse, Choice, Message, Usage


def create_choice(response_text: str) -> Choice:
    return Choice(
        index=0,
        message=Message(role="assistant", content=response_text),
        finish_reason="stop",
    )


def calculate_usage(prompt: str, result: str, tokenizer) -> Usage:
    prompt_tokens = len(tokenizer.encode(prompt))
    completion_tokens = len(tokenizer.encode(result))
    total_tokens = prompt_tokens + completion_tokens

    return Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )


def convert_result_to_response(
    model: str, prompt: str, result: str, tokenizer
) -> ChatCompletionResponse:
    return ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:10]}",
        object="chat.completion",
        created=int(time.time()),
        model=model,
        choices=[create_choice(response_text=result)],
        usage=calculate_usage(prompt=prompt, result=result, tokenizer=tokenizer),
    )
