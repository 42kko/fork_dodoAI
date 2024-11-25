import requests
import logging
from typing import Iterator, Optional, List, Dict, Any
import pprint
import asyncio

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatClient:
    """FastAPI 서버와 통신하는 채팅 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        ChatClient 초기화
        
        Args:
            base_url (str): API 서버 기본 URL
        """
        self.base_url = base_url.rstrip('/')
        
    def generate(self, repo_url: str, s3_path: str, include_test: bool, korean: bool) -> Dict[str, Any]:
        """
        문서 및 README 생성 API 요청
        
        Args:
            repo_url (str): 저장소 경로
            s3_path (str): S3 경로

        Returns:
            Dict[str, Any]: API 응답 데이터
        """
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

        except requests.RequestException as e:
            logger.error(f"문서 및 README 생성 API 요청 실패: {str(e)}")
            raise

    def chat(self, repo_name: str, query: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> Iterator[str]:
        """채팅 API 요청"""
        try:
            url = f"{self.base_url}/chat"
            payload = {
                "repo_url": repo_name,
                "query": query,
                "chat_history": chat_history or []
            }
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        yield chunk

        except requests.RequestException as e:
            logger.error(f"채팅 API 요청 실패: {str(e)}")
            raise


async def main():
    client = ChatClient()
    #repo_url = "https://github.com/aa-25/msung99.git"
    #repo_url = "https://github.com/spring-boot/spring-boot-projects.git"
    repo_url = "https://github.com/kakao-25/moheng.git"
    repo_name = "moheng"
    user_name = "kakao-25"

    #s3_path = "spring-boot-main.zip"
    #s3_path = "msung99-Gatsby-Starter-Haon"
    s3_path = "moheng-develop.zip"

    try:
        
        #문서 및 README 생성 테스트
        print("\n문서 및 README 생성 테스트:")
        generate_response = client.generate(repo_url=repo_url, s3_path=s3_path, include_test=False, korean=True)
        pprint.pprint(generate_response)
        
        
        # # 첫 번째 질문
        # query = "How to build this project? each frontend, backend, ai server. give me the command"
        # print(f"\n질문: {query}\n")
        # print("응답:")
        # full_response = ''
        
        # # 스트리밍 응답 처리
        # for response_chunk in client.chat(repo_name=repo_url, query=query):
        #     print(response_chunk, end='', flush=True)
        #     full_response += response_chunk
        
        # # 두 번째 질문: 이전 응답을 한국어로 번역 요청
        # print(f"\n\n질문: translate your answer to korean\n")
        # print("응답:")
        # chat_history = [
        #     {"role": "user", "content": query},
        #     {"role": "assistant", "content": full_response}
        # ]

        # # 번역 요청 스트리밍 처리
        # for response_chunk in client.chat(repo_name=repo_url, query="translate your answer to korean", chat_history=chat_history):
        #     print(response_chunk, end='', flush=True)
        
        
    except Exception as e:
        logger.error(f"테스트 실패: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())