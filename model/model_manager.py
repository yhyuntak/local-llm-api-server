import re
import ollama

class ModelManager:
    def __init__(self):
          # OpenAI 클라이언트 초기화 (Ollama 서버 가리키도록)
          self.client = ollama.Client()
          self.model_name = 'qwen3:14b'

    def generate(self, prompt: str, thinking: bool = False , **kwargs) -> ollama.GenerateResponse:
        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "stream": False,
                **kwargs,
            }
        )
        if not thinking:
            response.response = self._clean_thinking_tags(response.response)
        return response

    def _clean_thinking_tags(self, response: str) -> str:
      """빈 thinking 태그 제거"""
      # <think>\n\n</think>\n\n 패턴 제거
      cleaned = re.sub(r'<think>\s*</think>\s*', '', response, flags=re.DOTALL)
      # 추가 공백 정리
      return cleaned.strip()