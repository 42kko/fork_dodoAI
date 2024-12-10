from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
import time
import asyncio
from typing import Optional, List, Dict, Any, Tuple, Union
import os

from ktb_document_processor import DocumentProcessor
from ktb_api_client import APIClient
from ktb_utils import FileUtils, ImageProcessor
from ktb_settings import *
from ktb_chatbot import *
from ktb_func import *


origins = [
    "http://localhost:8080",
    "http://localhost:3000"
]

# 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# API 클라이언트 및 문서 프로세서 초기화
api_client = APIClient(os.getenv('OPENAI_API_KEY'))
doc_processor = DocumentProcessor(api_client)
file_utils = FileUtils()
image_processor = ImageProcessor()


class DocRequest(BaseModel):
    repo_url: str
    s3_path: str
    include_test: bool = False
    korean: bool = False
    blocks: List[str] = [
        "OVERVIEW_BLOCK",
        "STRUCTURE_BLOCK",
        "START_BLOCK",
        "MOTIVATION_BLOCK",
        "DEMO_BLOCK",
        "DEPLOYMENT_BLOCK",
        "CONTRIBUTORS_BLOCK",
        "FAQ_BLOCK",
        "PERFORMANCE_BLOCK"
    ]


class ChatRequest(BaseModel):
    repo_url: str
    query: str
    chat_history: Optional[List[Dict[str, Any]]] = None
    stream: bool = False


class ImageRequest(BaseModel):
    repo_url: str


def cleanup(repo_zip: str, clone_dir: str, doc_zip: str):
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


async def prepare_repository(repo_url: str, s3_path: str) -> Tuple[str, str, str, str]:
    """저장소 준비: URL 파싱, S3 다운로드, 압축 해제"""
    try:
        # 저장소 경로 파싱
        print("Repository preparation started")
        repo_name, user_name = parse_repo_url(repo_url)
        current_directory = os.getcwd()
        repo_path = os.path.join(current_directory, f"{repo_name}.zip")
        clone_dir = os.path.join(current_directory, f"{user_name}_{repo_name}")
        # S3에서 다운로드 및 압축 해제
        download_zip_from_s3(BUCKET_NAME, s3_path, repo_path)
        while not os.path.exists(repo_path):
            await asyncio.sleep(0.1)

        # 압축 해제 및 완료 확인
        extract_zip(repo_path, clone_dir)
        while not os.path.exists(clone_dir) or not os.listdir(clone_dir):
            await asyncio.sleep(0.1)

        print(f"Repository extraction completed: {clone_dir}")

        return repo_path, clone_dir, repo_name, user_name

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Repository preparation failed: {str(e)}"
        )


async def process_docs(directory_path: dict[str, list], output_directory: str, user_name: str, repo_name: str, korean: bool) -> bool:
    """문서 생성 및 요약 처리"""
    try:
        start_time = time.perf_counter()
        await doc_processor.generate_docs(directory_path, output_directory, korean)
        end_time = time.perf_counter()
        print(f"문서 생성 완료 처리 시간: {end_time - start_time} 초")
        await doc_processor.summarize_docs_async(output_directory, korean)
        end_time = time.perf_counter()
        print(f"문서 요약 완료 처리 시간: {end_time - start_time} 초")
        create_zip(output_directory, "Docs.zip")
        await upload_to_s3(BUCKET_NAME, "Docs.zip", f"{user_name}_{repo_name}_DOCS.zip")
        return True  # 성공적으로 완료되면 True 반환
    except Exception as doc_error:
        logger.error(f"문서 생성 중 오류 발생: {str(doc_error)}")
        return False  # 예외 발생 시 False 반환


async def perform_full_generation(repo_url, clone_dir, repo_name, user_name, include_test, korean, blocks):
    """문서 및 README 생성 작업을 백그라운드에서 수행"""
    try:
        start_time = time.perf_counter()

        # 파일 분석 및 처리
        java_files_path = file_utils.find_files(clone_dir, (".java",))
        java_categories = check_service_annotation(
            java_files_path, include_test)

        tasks = []
        readme_task = asyncio.create_task(doc_processor.process_readme(
            repo_url, clone_dir, user_name, repo_name, korean, blocks))
        tasks.append(readme_task)
        # java_categories가 있는 경우 문서 생성 태스크 추가
        doc_dir = os.path.join(clone_dir, "dododocs")
        if java_categories:
            docs_task = asyncio.create_task(process_docs(
                java_categories, doc_dir, user_name, repo_name, korean))
            tasks.append(docs_task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        readme_path, docs_dir = results if len(
            results) == 2 else (results[0], None)

        if not docs_dir or not readme_path:
            logger.error("문서 또는 README 생성 실패")
            raise Exception("문서 또는 README 생성 실패")

        await add_data_to_db(f"{repo_name}_generated", clone_dir, [".md"])

        end_time = time.perf_counter()
        print(f"문서 및 README 생성 시간: {end_time - start_time} 초")

    except Exception as e:
        logger.error(f"문서 및 README 생성 오류")


async def perform_readme_only_generation(repo_url, clone_dir, repo_name, user_name, korean, blocks):
    """README 생성 작업만 백그라운드에서 수행"""
    print(f"korean: {korean}")
    try:
        start_time = time.perf_counter()
        # README 생성
        readme = await doc_processor.process_readme(repo_url, clone_dir, user_name, repo_name, korean, blocks)
        if not readme:
            logger.error("README 생성 실패")
            raise Exception("README 생성 실패")

        await add_data_to_db(f"{repo_name}_generated", clone_dir, [".md"])

        end_time = time.perf_counter()
        print(f"README 생성 시간: {end_time - start_time} 초")

    except Exception as e:
        logger.error(f"README 생성 오류")


async def perform_tasks_and_cleanup(tasks, cleanup_args, db_name, clone_dir):
    """백그라운드 작업을 수행하고 완료되면 cleanup 실행"""
    await asyncio.gather(*tasks)  # 모든 백그라운드 작업이 완료될 때까지 대기
    # generated_files_dir = os.path.join(clone_dir, "dododocs")  # 생성된 파일이 저장된 디렉토리
    # await add_data_to_db(db_name, clone_dir, [".md"])  # 생성된 파일 저장
    print(f"add_data_to_db 완료: {db_name}, {clone_dir}")
    # await async_cleanup(*cleanup_args)  # cleanup 실행


@app.post("/generate")
async def generate(request: DocRequest, background_tasks: BackgroundTasks):
    """문서 및 README 생성 엔드포인트"""
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            # 1. Git 저장소 준비
            repo_dir, clone_dir, repo_name, user_name = await prepare_repository(
                request.repo_url,
                request.s3_path
            )
            # Java 파일 존재 여부 확인
            java_files_path = file_utils.find_files(clone_dir, (".java",))
            has_java_files = len(java_files_path) > 0
            print(f"has_java_files: {has_java_files}")
            # S3 키 생성
            readme_s3_key = f"{user_name}_{repo_name}_README.md"
            docs_s3_key = f"{user_name}_{repo_name}_DOCS.zip"

            # 백그라운드 작업 생성
            tasks = []
            if has_java_files:
                tasks.append(asyncio.create_task(
                    perform_full_generation(
                        request.repo_url, clone_dir, repo_name, user_name, request.include_test, request.korean, request.blocks)
                ))
                response = {"readme_s3_key": readme_s3_key,
                            "docs_s3_key": docs_s3_key}
            else:
                tasks.append(asyncio.create_task(
                    perform_readme_only_generation(
                        repo_dir, clone_dir, repo_name, user_name, request.korean, request.blocks)
                ))
                response = {"readme_s3_key": readme_s3_key,
                            "docs_s3_key": None}

            # 소스 파일들을 DB에 저장하는 작업 추가 (비동기)
            # BUILD_FILE_NAMES와 SRC_FILE_NAMES를 합치고 '.md'를 제외한 리스트 생성
            file_types = [ft for ft in SRC_FILE_NAMES if ft != '.md']
            print(f"total files : {len(file_types)}")
            source_db_task = asyncio.create_task(
                add_data_to_db(f"{repo_name}_source",
                               clone_dir, file_types)  # 소스 파일 저장
            )
            tasks.append(source_db_task)

            # 백그라운드에서 작업과 cleanup 실행
            background_tasks.add_task(perform_tasks_and_cleanup, tasks, (
                repo_dir, clone_dir, "Docs.zip"), f"{repo_name}_generated", clone_dir)

            return response

        except Exception as e:
            attempt += 1
            logger.error(f"문서 및 README 생성 오류 (시도 {
                         attempt}/{MAX_RETRIES}): {str(e)}")
            if attempt >= MAX_RETRIES:
                logger.error("최대 재시도 횟수에 도달했습니다. 작업을 중단합니다.")
            else:
                logger.info(f"{RETRY_DELAY}초 후에 재시도합니다...")
                await asyncio.sleep(RETRY_DELAY)  # 재시도 간격 대기
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"문서 및 README 생성 오류: {str(e)}"
    )


@app.post("/generate_develop")
async def generate_develop(request: DocRequest, background_tasks: BackgroundTasks):
    """문서 및 README 생성 엔드포인트"""
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            # 1. Git 저장소 준비
            repo_dir, clone_dir, repo_name, user_name = await prepare_repository(
                request.repo_url,
                request.s3_path
            )
            # Java 파일 존재 여부 확인
            java_files_path = file_utils.find_files(clone_dir, (".java",))
            has_java_files = len(java_files_path) > 0
            print(f"has_java_files: {has_java_files}")
            # S3 키 생성
            readme_s3_key = f"{user_name}_{repo_name}_README.md"
            docs_s3_key = f"{user_name}_{repo_name}_DOCS.zip"

            # 백그라운드 작업 생성
            tasks = []
            tasks.append(asyncio.create_task(
                perform_readme_only_generation(
                    request.repo_url, clone_dir, repo_name, user_name, request.korean, request.blocks)
            ))
            response = {"readme_s3_key": readme_s3_key,
                        "docs_s3_key": None}

            # 백그라운드에서 작업과 cleanup 실행
            background_tasks.add_task(perform_tasks_and_cleanup, tasks, (
                repo_dir, clone_dir, "Docs.zip"), f"{repo_name}_generated", clone_dir)

            return response

        except Exception as e:
            attempt += 1
            logger.error(f"문서 및 README 생성 오류 (시도 {
                         attempt}/{MAX_RETRIES}): {str(e)}")
            if attempt >= MAX_RETRIES:
                logger.error("최대 재시도 횟수에 도달했습니다. 작업을 중단합니다.")
            else:
                logger.info(f"{RETRY_DELAY}초 후에 재시도합니다...")
                await asyncio.sleep(RETRY_DELAY)  # 재시도 간격 대기
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"문서 및 README 생성 오류: {str(e)}"
    )


@app.post("/chat")
async def chat(request: ChatRequest):
    """채팅 엔드포인트"""
    try:
        if not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )

        # chat_history가 딕셔너리로 주어졌을 때 변환
        if request.chat_history:
            chat_history = []
            for item in request.chat_history:
                chat_history.append(
                    {"role": "user", "content": item["question"]})
                chat_history.append(
                    {"role": "assistant", "content": item["answer"]})
            response = codebase_chat(
                request.query,
                request.repo_url,
                chat_history,
                request.stream
            )
        else:
            response = codebase_chat(
                request.query,
                request.repo_url,
                request.chat_history,
                request.stream
            )

        if request.stream:
            return StreamingResponse(
                response,
                media_type="text/plain"
            )
        else:
            return {"answer": response}

    except Exception as error:
        logger.error(f"채팅 오류: {str(error)}", exc_info=True)
        return {"answer": f"Error: {str(error)}"}


async def test(task_name: str):
    """비동기 백그라운드 작업"""
    await asyncio.sleep(2)  # 비동기 작업 예시
    print(f"{task_name} 완료")


@app.post("/generate_image")
async def generate_image(request: ImageRequest):
    """이미지 생성 엔드포인트"""
    try:
        repo_name, user_name = parse_repo_url(request.repo_url)
        s3_path = f"{user_name}_{repo_name}_README.md"
        current_directory = os.getcwd()
        repo_path = os.path.join(current_directory, s3_path)
        download_zip_from_s3(BUCKET_NAME, s3_path, repo_path)

        description = image_processor.read_description_from_readme(s3_path)
        image_url, image_path = image_processor.generate_image(description)

        return {"image_url": image_url}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"오류 발생: {str(e)}"
        )
    finally:
        if os.path.exists(repo_path):
            os.remove(repo_path)
        if os.path.exists(image_path):
            os.remove(image_path)


@app.post("/test")
async def tttest():
    """문서 및 README 생성 엔드포인트"""
    try:
        # 비동기 백그라운드 작업 생성
        asyncio.create_task(test("Task 1"))
        asyncio.create_task(test("Task 2"))

        # 클라이언트에 즉시 응답 반환
        return {"message": "백그라운드 작업이 시작되었습니다."}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"오류 발생: {str(e)}"
        )


@app.get("/ping")
async def ping():
    try:
        return JSONResponse(status_code=200, content={"message": "pong"})
    except Exception as e:
        # 오류 발생 시 예외 처리
        raise HTTPException(
            status_code=500,
            detail=f"오류 발생: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "ktb_server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,
        workers=1
    )
