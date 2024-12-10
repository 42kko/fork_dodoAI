from ktb_settings import *
from ktb_func import *

import re
import os
from urllib.parse import urlparse
import zipfile
import logging
import shutil
import boto3
import asyncio


logger = logging.getLogger(__name__)
"""**FUNCTIONS**"""


def check_service_annotation(java_files, include_tests=INCLUDE_TEST):
    """
    Java 파일들을 어노테이션 타입별로 분류하여 딕셔너리로 반환
    """
    classified_files = {
        'Controller': [],
        'Test': []
    }
    # 각 어노테이션별 패턴
    patterns = {
        'Controller': re.compile(r'@(?:Controller|RestController)\b'),
        'Test': re.compile(r'@Test\b')
    }

    for file in java_files:
        if os.path.isfile(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 각 어노테이션 타입 검사
                    for annotation, pattern in patterns.items():
                        if pattern.search(content):
                            if annotation == 'Test' and not include_tests:
                                continue
                            classified_files[annotation].append(file)
            except Exception as e:
                logger.error(f"파일 읽기 오류 {file}: {str(e)}")
                continue

    print(f"전체 파일 수: {len(java_files)}")
    # 결과 로깅
    for annotation, files in classified_files.items():
        print(f"{annotation} 파일 수: {len(files)}")

    total_files = sum(len(files) for files in classified_files.values())
    print(f"전체 어노테이션 파일 수: {total_files}")

    return classified_files


def parse_repo_url(repo_url: str):
    # URL 파싱
    parsed_url = urlparse(repo_url)

    # path에서 'user/repo.git' 추출 후 처리
    path_parts = parsed_url.path.strip('/').split('/')

    if len(path_parts) != 2:
        raise ValueError(f"잘못된 레포지토리 URL: {repo_url}")

    user_name, repo_name = path_parts
    repo_name = repo_name.replace('.git', '')  # '.git' 제거

    return repo_name, user_name


def download_zip_from_s3(BUCKET_NAME, object_key, download_path):
    """S3에서 ZIP 파일을 다운로드"""
    # 다운로드 경로의 디렉토리 부분 추출
    download_dir = os.path.dirname(download_path)
    # 디렉토리가 없으면 생성
    if download_dir and not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"디렉토리 생성됨: {download_dir}")
    try:
        # 파일 다운로드
        print(f"파일 다운로드 시작: {object_key}, {download_path}")
        s3.download_file(BUCKET_NAME, object_key, download_path)
        print(f"파일이 성공적으로 다운로드되었습니다: {object_key}")
    except Exception as e:
        print(f"파일 다운로드 중 오류 발생: {str(e)}")
    # s3.download_file(BUCKET_NAME, object_key, download_path)


def extract_zip(file_path, extract_to):
    """ZIP 파일의 압축 해제"""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def create_zip(directory, zip_path):
    """디렉토리의 모든 파일을 ZIP으로 압축"""
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zip_ref.write(file_path, os.path.relpath(file_path, directory))


async def async_cleanup(repo_zip: str, clone_dir: str, doc_zip: str):
    """임시 파일 및 디렉토리 정리"""
    try:
        # repo_zip 파일 삭제
        if repo_zip and os.path.exists(repo_zip):
            os.remove(repo_zip)
            print(f"Removed repo zip file: {repo_zip}")

        # ZIP 파일 삭제
        if doc_zip and os.path.exists(doc_zip):
            os.remove(doc_zip)
            print(f"Removed zip file: {doc_zip}")

        # 클론 디렉토리 삭제
        if clone_dir and os.path.exists(clone_dir):
            shutil.rmtree(clone_dir)
            print(f"Removed clone directory: {clone_dir}")

    except Exception as e:
        print(f"Cleanup failed: {str(e)}")


async def upload_to_s3(bucket: str, file_path: str, key: str):
    """S3에 파일 업로드"""
    try:
        with open(file_path, 'rb') as file:
            await asyncio.to_thread(
                s3.upload_fileobj,
                file,
                bucket,
                key
            )
    except Exception as e:
        logger.error(f"S3 업로드 실패: {str(e)}")
        raise Exception(f"S3 업로드 실패: {str(e)}")


def remove_markdown_blocks(content):
    content = content.replace("```markdown", "")
    content = content.replace(f"```\n```", "```")
    return content
