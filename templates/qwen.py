from typing import List

from chat.models import Message
from templates.base import ChatTemplate


class QwenTemplate(ChatTemplate):
    # qwen2.5 7b
    def convert_messages(self, messages: List[Message]) -> str:
        prompt = ""
        for message in messages:
            prompt += f"<|im_start|>{message.role}\n{message.content}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"
        return prompt
