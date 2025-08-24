from abc import ABC, abstractmethod
from typing import List

from chat.models import Message


class ChatTemplate(ABC):
    @abstractmethod
    def convert_messages(self, messages: List[Message]) -> str:
        pass
