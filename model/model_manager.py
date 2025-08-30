import asyncio
import re
import ollama
import aiohttp
from concurrent.futures import ThreadPoolExecutor

class ModelManager:
    def __init__(self):
          # OpenAI 클라이언트 초기화 (Ollama 서버 가리키도록)
          self.client = ollama.Client()
          self.model_name = 'qwen3:14b'
          # 공유 ClientSession 생성
          self.session = None

    async def get_session(self):
        """공유 세션 반환 (없으면 생성)"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120),
                connector=aiohttp.TCPConnector(limit=100, limit_per_host=20)
            )
        return self.session

    async def generate(self, prompt: str, thinking: bool = False , **kwargs) -> ollama.GenerateResponse:
        import time
        start_time = time.time()
        print(f"🔵 ModelManager.generate() 시작: {start_time:.2f}")
        
        # aiohttp로 직접 OLLAMA API 호출 (공유 세션 사용)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": kwargs
        }
        
        session = await self.get_session()
        print(f"🟡 OLLAMA 요청 전송: {time.time():.2f}")
        async with session.post(
            "http://localhost:11434/api/generate",
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                
                # ollama.GenerateResponse와 호환되는 객체 생성
                result = ollama.GenerateResponse(
                    model=data.get('model', self.model_name),
                    created_at=data.get('created_at', ''),
                    response=data.get('response', ''),
                    done=data.get('done', True),
                    context=data.get('context', []),
                    total_duration=data.get('total_duration', 0),
                    load_duration=data.get('load_duration', 0),
                    prompt_eval_count=data.get('prompt_eval_count', 0),
                    prompt_eval_duration=data.get('prompt_eval_duration', 0),
                    eval_count=data.get('eval_count', 0),
                    eval_duration=data.get('eval_duration', 0)
                )
                
                # thinking 태그 제거 임시 비활성화 (테스트용)
                if not thinking:
                    result.response = self._clean_thinking_tags(result.response)
                
                end_time = time.time()
                print(f"🟢 ModelManager.generate() 완료: {end_time:.2f} (소요시간: {end_time - start_time:.2f}초)")
                return result
            else:
                raise Exception(f"OLLAMA API error: {response.status}")


    def _clean_thinking_tags(self, response: str) -> str:
      """빈 thinking 태그 제거"""
      # <think>\n\n</think>\n\n 패턴 제거
      cleaned = re.sub(r'<think>\s*</think>\s*', '', response, flags=re.DOTALL)
      # 추가 공백 정리
      return cleaned.strip()