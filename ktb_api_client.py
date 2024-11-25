"""API 클라이언트 관련 코드"""
import aiohttp
from typing import Optional, List, Dict
import asyncio
import logging  # 추가
from ktb_settings import *


logger = logging.getLogger(__name__)  # 추가

class APIClient:
    """API 요청 처리 클래스"""
    def __init__(self, api_key: str, model: str = MODEL, temperature: float = TEMPERATURE):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def _prepare_request(self, prompt: str, content: str) -> dict:
        """API 요청 데이터 준비"""
        messages = self._chat_format(prompt, content)
        return self._get_json_data(messages=messages)

    def _chat_format(self, prompt: str, content: str) -> list[dict[str, str]]:
        """채팅 메시지 포맷 구성"""
        if self.model.startswith("gpt"):
            system_role = "system"
        elif self.model.startswith("claude"):
            system_role = "model"
        else:
            system_role = "assistant"

        return [
            {"role": system_role, "content": prompt},
            {"role": "user", "content": content}
        ]

    def _get_json_data(
        self,
        messages: List[Dict[str, str]],
        stop: Optional[List[str]] = None,
        seed: Optional[int] = None,
        tools: Optional[List] = None,
        logprobs: Optional[int] = None,
        top_logprobs: Optional[Dict[str, float]] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, any]:
        """API 요청 JSON 데이터 생성"""
        params = {
            "model": GPT_MODEL,
            "messages": messages,
            "temperature": self.temperature
        }
        
        if self.model.startswith("claude"):
            params["max_tokens"] = max_tokens or 8192
            if stop:
                params["stop_sequences"] = stop
        else:
            if stop:
                params["stop"] = stop
            if logprobs:
                params["logprobs"] = logprobs
            if top_logprobs:
                params["top_logprobs"] = top_logprobs
            if seed:
                params["seed"] = seed
            if tools:
                params["tools"] = tools
            if max_tokens:
                params["max_tokens"] = max_tokens
        
        return params

    async def generate_text(self, session: aiohttp.ClientSession, 
                            prompt: str, content: str, max_retries: int = MAX_RETRIES) -> Optional[str]:
        """텍스트 생성 API 호출"""
        attempt = 0
        while attempt < max_retries:
            try:
                json_data = self._prepare_request(prompt, content)
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    json=json_data,
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        logger.error(f"API 오류: {response.status} - {error_text}")
                        if response.status in {502, 503, 504}:
                            # 일시적인 서버 오류일 경우 재시도
                            attempt += 1
                            logger.info(f"재시도 {attempt}/{max_retries}...")
                            await asyncio.sleep(2 ** attempt)  # 지수 백오프
                        else:
                            raise Exception(f"API 오류: {response.status} - {error_text}")
            except Exception as e:
                logger.error(f"API 호출 오류: {str(e)}")
                logger.error("스택 트레이스:", exc_info=True)
                return None
        return None

    async def process_chunks(self, chunks: List[str], prompt: str,
                           batch_size: int = 50) -> List[str]:
        """청크 배치 처리"""
        results = []
        async with aiohttp.ClientSession() as session:
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                batch_results = await asyncio.gather(*[
                    self.generate_text(session, prompt, chunk)
                    for chunk in batch
                ])
                results.extend([r for r in batch_results if r is not None])
                await asyncio.sleep(40)  # Rate limit 회피
        return results 