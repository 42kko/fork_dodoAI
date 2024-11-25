from typing import List, Optional
import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import tiktoken
import aiofiles
from token_chunker import *
from ktb_settings import *
import io
import requests
from PIL import Image
import re

from ktb_settings import client_gpt
from ktb_prompts import DALLE_PROMPT

logger = logging.getLogger(__name__)

class FileUtils:
    """파일 처리 관련 유틸리티"""
    @staticmethod
    def find_files(directory: str, extensions: tuple) -> List[str]:
        """지정된 확장자를 가진 파일들을 찾음"""
        files = []
        for root, _, filenames in os.walk(directory):
            #if any(excl in root for excl in EXCLUDE_DIRS):
            #    continue
            files.extend(
                os.path.join(root, f) 
                for f in filenames 
                if f.endswith(extensions)
            )
        return files

class TextProcessor:
    """텍스트 처리 관련 유틸리티"""
    @staticmethod
    def count_tokens(text: str) -> int:
        try:
            encoding = tiktoken.encoding_for_model(GPT_MODEL)
            return len(encoding.encode(text, disallowed_special=()))
        except Exception as e:
            logger.error(f"토큰 계산 오류: {str(e)}")
            return len(text) // 4

    @staticmethod
    def split_text(text: str, max_tokens: int = GPT_MAX_TOKENS) -> List[str]:
        return chunker.chunk(text)

class AsyncFileIO:
    """비동기 파일 입출력 처리"""
    def __init__(self):
        self.io_pool = ThreadPoolExecutor(
            max_workers=multiprocessing.cpu_count() * 2
        )

    async def save_file(self, path: str, content: str):
        """비동기로 파일 저장"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self.io_pool,
            lambda: open(path, "w", encoding="utf-8").write(content)
        )

    async def read_file(self, path: str) -> str:
        """비동기로 파일 읽기"""
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read() 

class ImageProcessor:
    """이미지 생성 및 README 업데이트 관련 유틸리티"""

    def __init__(self):
        self.client_gpt = client_gpt
        self.dalle_prompt = DALLE_PROMPT

    def read_description_from_readme(self, file_path="README.md"):
        """README 파일에서 'Overview' 섹션 추출"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                # Description 섹션을 정규 표현식으로 추출
                description_match = re.search(r"Overview\n(.*?)(### Main Purpose)", content, re.S)

                if description_match:
                    return description_match.group(1).strip()
                else:
                    raise ValueError("Could not find 'Overview' or 'Main Purpose' sections in the README.md")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        
    def generate_image(self, description, new_size=(400, 400)):
        """DALL-E를 사용하여 이미지 생성"""
        response = self.client_gpt.images.generate(
            model="dall-e-3",
            prompt=self.dalle_prompt + description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        image_data = requests.get(image_url).content

        img = Image.open(io.BytesIO(image_data))
        resized_img = img.resize(new_size)

        image_path = f"generated_image.png"
        resized_img.save(image_path)

        return image_url, image_path

    def update_readme_with_image(self, file_path="README.md", image_path="./generated_image.png"):
        """README 파일에 이미지 삽입"""
        with open(file_path, "r+", encoding="utf-8") as file:
            content = file.read()

            # 'Preview' 섹션 뒤에 이미지를 삽입
            new_content = re.sub(
                r"(Preview\n)(.*?)(##|$)",
                f"Preview\n\n<img src='{image_path}' width='400' height='400'/>\n\n\\3",
                content, flags=re.S
            )

            # 파일에 변경 사항 쓰기
            file.seek(0)
            file.write(new_content)
            file.truncate()
