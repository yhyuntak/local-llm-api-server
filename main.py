import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from fastapi import FastAPI
from mlx_lm import generate, load
from pydantic import BaseModel

#   1. 요청 구조 (POST /v1/chat/completions)
#   {
#     "model": "gpt-3.5-turbo",
#     "messages": [
#       {"role": "user", "content": "Hello, how are you?"}
#     ],
#     "temperature": 0.7,
#     "max_tokens": 150
#   }

#   2. 응답 구조
#   {
#     "id": "chatcmpl-123",
#     "object": "chat.completion",
#     "created": 1677652288,
#     "model": "gpt-3.5-turbo",
#     "choices": [
#       {
#         "index": 0,
#         "message": {"role": "assistant", "content": "Hello! I'm doing well, thank you for asking..."},
#         "finish_reason": "stop"
#       }
#     ],
#     "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21}
#   }


class Message(BaseModel):
    role: str  # "system", "user", "assistant"
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 100
    top_p: Optional[float] = 1.0
    repetition_penalty: Optional[float] = 0.0  # frequency_penalty 대신 (반복 억제)


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class ChatTemplate(ABC):
    @abstractmethod
    def convert_messages(self, messages: List[Message]) -> str:
        pass


class QwenTemplate(ChatTemplate):
    # qwen2.5 7b
    def convert_messages(self, messages: List[Message]) -> str:
        prompt = ""
        for message in messages:
            prompt += f"<|im_start|>{message.role}\n{message.content}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"
        return prompt


def get_chat_template(model_name: str) -> ChatTemplate:
    if str.startswith(model_name.lower(), "qwen"):
        return QwenTemplate()
    else:
        return QwenTemplate()


def qwen_template(messages: List[Message]) -> str:
    prompt = ""
    for message in messages:
        prompt += f"<|im_start|>{message.role}\n{message.content}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt


TEMPLATES = {"qwen": qwen_template}


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


class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model(self):
        self.model, self.tokenizer = load(
            "/Users/yoohyuntak/workspace/models/mlx/Qwen2.5-7B-Instruct"
        )


modelManager = ModelManager()


app = FastAPI(
    title="Local LLM API Server",
    description="로컬 MLX LLM 모델을 위한 OpenAI 호환 API 서버",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    print("Loading model...")
    modelManager.load_model()
    print("Model loaded!")


@app.get("/")
async def root():
    return {"message": "Local LLM API Server is running!"}


@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
) -> Optional[ChatCompletionResponse]:
    # Strategy + Factory Pattern 방식
    template = get_chat_template(request.model)
    prompt = template.convert_messages(request.messages)

    # 딕셔너리 방식
    # template = TEMPLATES.get("qwen",qwen_template) # 뒤는 default 값
    # prompt = template(request.messages)

    result = generate(
        modelManager.model,
        modelManager.tokenizer,
        prompt=prompt,
        verbose=True,
        max_tokens=request.max_tokens,
    )
    return convert_result_to_response(
        model=request.model,
        prompt=prompt,
        result=result,
        tokenizer=modelManager.tokenizer,
    )
