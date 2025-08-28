from typing import List, Optional

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
    num_predict: Optional[int] = 100
    repeat_penalty: Optional[float] = 0.0  # frequency_penalty 대신 (반복 억제)
    temperature: Optional[float] = 0.0
    top_k: Optional[int] = 20
    top_p: Optional[float] = 1.0
    thinking: Optional[bool] = False


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
