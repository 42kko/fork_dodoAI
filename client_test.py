import requests
import logging
from typing import Iterator, Optional, List, Dict, Any, Union
import pprint
import asyncio
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatClient:
    """FastAPI 서버와 통신하는 채팅 클라이언트"""

    def __init__(self, base_url: str = None):
        """
        ChatClient 초기화

        Args:
            base_url (str): API 서버 기본 URL
        """
        self.base_url = base_url or os.getenv(
            "API_BASE_URL", "http://localhost:8000").rstrip('/')

    def generate(self, repo_url: str, s3_path: str, include_test: bool = False, korean: bool = False) -> Dict[str, Any]:
        """문서 및 README 생성 API 요청"""
        try:
            url = f"{self.base_url}/generate"
            payload = {
                "repo_url": repo_url,
                "s3_path": s3_path,
                "include_test": include_test,
                "korean": korean
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.ConnectionError:
            logger.error("서버에 연결할 수 없습니다.")
            raise
        except requests.Timeout:
            logger.error("요청 시간이 초과되었습니다.")
            raise
        except requests.RequestException as e:
            logger.error(f"문서 및 README 생성 API 요청 실패: {str(e)}")
            raise

    def chat(self, repo_name: str, query: str, chat_history: Optional[List[Dict[str, Any]]] = None, stream: bool = False) -> Union[str, Iterator[str]]:
        """채팅 API 요청"""
        try:
            url = f"{self.base_url}/chat"
            payload = {
                "repo_url": repo_name,
                "query": query,
                "chat_history": chat_history or [],
                "stream": stream
            }

            response = requests.post(url, json=payload, stream=stream)
            response.raise_for_status()

            if stream:
                return self._stream_response(response)
            else:
                # JSON 응답에서 answer 필드 추출
                return response.json()["answer"]

        except requests.RequestException as e:
            logger.error(f"채팅 API 요청 실패: {str(e)}")
            raise

    def _stream_response(self, response) -> Iterator[str]:
        """스트리밍 응답 처리"""
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


async def main():
    client = ChatClient()
    # repo_url = "https://github.com/aa-25/msung99.git"
    # repo_url = "https://github.com/spring-boot/spring-boot-projects.git"
    repo_url = "https://github.com/kakao-25/moheng.git"
    repo_name = "moheng"
    user_name = "kakao-25"

    # s3_path = "spring-boot-main.zip"
    # s3_path = "msung99-Gatsby-Starter-Haon"
    s3_path = "moheng-develop.zip"

    # 첫 번째 질문
    query = "describe AuthController and its response/endpoint"
    print(f"\n질문: {query}\n")
    print("응답:")

    # 응답 처리
    response = client.chat(repo_name=repo_url, query=query, stream=False)
    print(response)

    # 채팅 기록 예시
    chat_history = [
        {
            "question": query,
            "answer": response
        }
    ]
    # 추가 질문 처리...

if __name__ == "__main__":
    asyncio.run(main())
