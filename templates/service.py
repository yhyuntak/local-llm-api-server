from templates.base import ChatTemplate
from templates.qwen import QwenTemplate


def get_chat_template(model_name: str) -> ChatTemplate:
    if str.startswith(model_name.lower(), "qwen"):
        return QwenTemplate()
    else:
        return QwenTemplate()
