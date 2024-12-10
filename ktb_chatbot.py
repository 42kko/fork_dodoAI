from ktb_prompts import *
from ktb_settings import *
from ktb_func import *

import os
from typing import List, Dict, Optional, Any, Generator, Union
from pathlib import Path
import logging
import tiktoken
import aiofiles
from itertools import tee

"""**FUNCTION FOR CHAT**"""
# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def search_file(repo_path, filename):
    repo_path = Path(repo_path)

    # 경로 안의 모든 파일과 폴더를 탐색
    for file_path in repo_path.rglob(filename):
        return file_path  # 첫 번째로 찾은 파일 반환

    return None  # 파일이 없으면 None 반환


async def process_file(file_path: Path, vector_store, file_metadata, chunk_id_counter: int) -> int:
    """파일을 처리하고 벡터 스토어에 추가"""
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            doc = await file.read()
            if doc.strip():
                if file_path.suffix == '.md':
                    chunks = embedding_chunker.chunk(doc)
                    if chunks:
                        chunk_contents = [
                            chunk.text.replace('\n', ' ').strip()
                            for chunk in chunks if chunk.text.strip()
                        ]
                        if chunk_contents:
                            chunk_ids = [
                                f"{file_path}_{i}"
                                for i in range(chunk_id_counter, chunk_id_counter + len(chunk_contents))
                            ]
                            chunk_metadatas = [
                                file_metadata for _ in range(len(chunk_contents))]
                            vector_store.add(
                                documents=chunk_contents,
                                metadatas=chunk_metadatas,
                                ids=chunk_ids
                            )
                            # print(f"Successfully processed file: {
                            #       file_metadata["filename"]} - Added {len(chunks)} chunks")
                            return len(chunk_contents)
                else:
                    if len(tiktoken.encoding_for_model(EMBEDDING_MODEL).encode(doc)) <= 8191:
                        # print(f"file: {file_metadata["filename"]} len: {
                        #       len(tiktoken.encoding_for_model(EMBEDDING_MODEL).encode(doc))}")
                        vector_store.add(
                            documents=[doc.replace('\n', ' ').strip()],
                            metadatas=[file_metadata],
                            ids=[f"{file_path}"]
                        )
                        # print(f"Successfully processed file: {
                        #       file_metadata["filename"]}")
                        return 1
                    else:
                        # print(f"will chunk file: {file_metadata["filename"]} len: {
                        #       len(tiktoken.encoding_for_model(EMBEDDING_MODEL).encode(doc))}")
                        max_chunk_size = 8192
                        overlap_size = 100
                        chunks = [
                            doc[i:i + max_chunk_size]
                            for i in range(0, len(doc), max_chunk_size - overlap_size)
                        ]
                        chunk_ids = [
                            f"{file_path}_{i}"
                            for i in range(chunk_id_counter, chunk_id_counter + len(chunks))
                        ]
                        chunk_metadatas = [
                            file_metadata for _ in range(len(chunks))]
                        vector_store.add(
                            documents=chunks,
                            metadatas=chunk_metadatas,
                            ids=chunk_ids
                        )
                        print(f"Successfully processed file: {
                              file_metadata["filename"]} - Added {len(chunks)} chunks")
                        return len(chunks)
    except UnicodeDecodeError as e:
        logger.error(f"Unicode decode error in file {file_path}: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")
    return 0


async def add_data_to_db(db_name: str, path: str, file_type: List[str]) -> int:
    """DB에 데이터를 추가"""
    try:
        vector_store = chroma_client.get_or_create_collection(
            name=db_name,
            embedding_function=embedding_function,
            metadata=DISTANCE
        )
        repo_path = Path(path)
        total_files_processed = 0
        chunk_id_counter = 0
        for root, dirs, files in os.walk(repo_path):
            for filename in files:
                if filename == '.DS_Store':
                    continue
                if any(filename.endswith(ft) or filename == ft for ft in file_type):
                    file_path = search_file(repo_path, filename)
                    if file_path and file_path.exists() and file_path.is_file():
                        file_metadata = {
                            "filename": filename,
                            "path": str(file_path),
                            "repository": db_name
                        }
                        chunks_added = await process_file(file_path, vector_store, file_metadata, chunk_id_counter)
                        chunk_id_counter += chunks_added
                        if chunks_added > 0:
                            total_files_processed += 1
        if total_files_processed == 0:
            logger.error("No valid files were processed")
            return 0

        total_chunks = vector_store.count()
        print(f"Successfully processed {total_files_processed} files with total {
              total_chunks} chunks in {db_name}")
        return total_chunks
    except Exception as e:
        logger.error(f"Error adding data to DB: {str(e)}")
        raise


def db_search(query: str, db: Any, n_results: int = 3) -> Dict[str, Any]:
    """
    Search the vector database for similar documents.

    Args:
        query (str): Search query
        db: ChromaDB collection
        n_results (int): Number of results to return
        threshold (float): Similarity threshold

    Returns:
        Dict[str, Any]: Search results including documents and metadata
    """
    try:
        results = db.query(
            query_texts=query,
            n_results=n_results
        )
        return results

    except Exception as e:
        logger.error(f"Error searching DB: {str(e)}")
        raise


def generate_response(query: str, db_list: List[Any], chat_history: Optional[List[dict]] = None, augmented_query: Optional[str] = None, stream: bool = False) -> str:
    """Generate a response using LLM based on retrieved documents."""
    try:
        if augmented_query:
            retrieved_docs_source = db_search(augmented_query, db_list[0])
            retrieved_docs_generated = db_search(augmented_query, db_list[1])
        else:
            retrieved_docs_source = db_search(query, db_list[0])
            retrieved_docs_generated = db_search(query, db_list[1])

        system_prompt = CHATBOT_PROMPT
        user_prompt = f"""
Retrieved Content:
{retrieved_docs_source['documents']}

{retrieved_docs_generated['documents']}

User Query / Instruct: {query}
"""
        full_prompt = [{"role": "system", "content": system_prompt}]
        if chat_history:
            full_prompt.extend(chat_history)
        full_prompt.append({"role": "user", "content": user_prompt})

        client_gpt = get_openai_client()
        response = client_gpt.chat.completions.create(
            model=GPT_MODEL,
            messages=full_prompt,
            temperature=0.52,
            stream=False  # 항상 스트리밍 비활성화
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise


def stream_response(query: str, db_list: List[Any], chat_history: Optional[List[dict]] = None, augmented_query: Optional[str] = None) -> Generator:
    """Generate a streaming response."""
    try:
        if augmented_query:
            retrieved_docs_source = db_search(augmented_query, db_list[0])
            retrieved_docs_generated = db_search(augmented_query, db_list[1])
        else:
            retrieved_docs_source = db_search(query, db_list[0])
            retrieved_docs_generated = db_search(query, db_list[1])

        system_prompt = CHATBOT_PROMPT
        user_prompt = f"""
Retrieved Content:
{retrieved_docs_source['documents']}

{retrieved_docs_generated['documents']}

User Query / Instruct: {query}
"""
        full_prompt = [{"role": "system", "content": system_prompt}]
        if chat_history:
            full_prompt.extend(chat_history)
        full_prompt.append({"role": "user", "content": user_prompt})

        client_gpt = get_openai_client()
        response = client_gpt.chat.completions.create(
            model=GPT_MODEL,
            messages=full_prompt,
            temperature=0.52,
            stream=True  # 항상 스트리밍 활성화
        )

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        logger.error(f"Error generating streaming response: {str(e)}")
        raise


def evaluate_response(response: str) -> bool:
    """
    응답의 적절성을 평가하는 함수.
    적절하지 않으면 False를 반환하여 쿼리 증강을 유도합니다.

    Args:
        response (str): 생성된 응답

    Returns:
        bool: 응답이 적절하면 True, 그렇지 않으면 False
    """
    # 간단한 평가 기준 예시: 응답이 비어있거나 특정 키워드를 포함하지 않으면 False
    if not response or "Error" in response or "not found" in response:
        return False
    return True


def codebase_chat(query: str, repo_url: str, chat_history: List[dict] = None, stream: bool = False) -> Union[str, Generator]:
    """채팅 응답 생성"""
    try:
        repo_name, _ = parse_repo_url(repo_url)
        vector_store_source = chroma_client.get_collection(
            name=f"{repo_name}_source",
            embedding_function=embedding_function
        )
        vector_store_generated = chroma_client.get_collection(
            name=f"{repo_name}_generated",
            embedding_function=embedding_function
        )
        db_list = [vector_store_source, vector_store_generated]

        if chat_history:
            total_content = ''.join([msg['content']
                                    for msg in chat_history]) + query
            total_tokens = len(tiktoken.encoding_for_model(
                GPT_MODEL).encode(total_content))
            last_message = chat_history[-1] if total_tokens > MAX_TOKEN_LENGTH else chat_history
        else:
            last_message = None

        augmented_query = query_augmentation(query, last_message)

        if stream:
            return stream_response(query, db_list, last_message, augmented_query)
        else:
            return generate_response(query, db_list, last_message, augmented_query, stream)

    except Exception as e:
        logger.error(f"Error in codebase chat: {str(e)}")
        raise


def query_augmentation(query: str, chat_history: Optional[List[dict]] = None) -> str:
    """
    주어진 쿼리와 이전 응답을 분석하여 추가 검색이 필요한 정보를 식별하고 검색 쿼리를 생성합니다.

    Args:
        query (str): 사용자 입력 쿼리
        previous_query (str): 이전 쿼리 내용
        previous_response (str): 이전 응답 내용
    Returns:
        str: 증강된 검색 쿼리
    """
    prompt = AUGMENTATION_PROMPT

    if chat_history and len(chat_history) >= 2:
        previous_query = chat_history[-2]['content']
        previous_response = chat_history[-1]['content']
    else:
        previous_query = ""
        previous_response = ""

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Previous Query: {
            previous_query}\nPrevious Response: {previous_response}\nQuery: {query}"}
    ]
    client_gpt = get_openai_client()
    augmented_query = client_gpt.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0.52,
        max_tokens=150,
    )

    return augmented_query.choices[0].message.content


def should_augment_query(response: str) -> bool:
    if "Error" in response or "not found" in response:
        return True
    return False
# # 사용 예시
# query = """how can i use this api? and how can i fix Error 404"""
# response = """To use the API, you can follow these general steps based on the provided context:

# ### Using the API

# 1. **Authentication**:
#    - Obtain an access token through OAuth by following the login process with your chosen OAuth provider (e.g., Kakao, Google).
#    - Use the generated access token for subsequent API requests.

# 2. **Making Requests**:
#    - Use tools like Postman or libraries like RestAssured (as shown in the `RecommendTripAcceptenceFixture` and `KeywordAcceptenceFixture` classes) to make HTTP requests to the API endpoints.
#    - Ensure you set the correct HTTP method (GET, POST, DELETE) and include the access token in the authorization header.

# 3. **Example Requests**:
#    - To select a preferred trip:
#      ```java
#      ExtractableResponse<Response> response = RecommendTripAcceptenceFixture.선호_여행지를_선택한다(tripId, accessToken);
#      ```
#    - To retrieve AI-customized recommended trips:
#      ```java
#      ExtractableResponse<Response> response = RecommendTripAcceptenceFixture.AI_맞춤_추천_여행지를_조회한다(accessToken);
#      ```

# ### Fixing Error 404

# A 404 error typically indicates that the requested resource could not be found. Here are some steps to troubleshoot and fix this error:

# 1. **Check the Endpoint**: Ensure that you are using the correct URL for the API endpoint. Refer to the API documentation or the provided context to verify the endpoint paths.

# 2. **Verify HTTP Method**: Make sure you are using the correct HTTP method (GET, POST, DELETE) as required by the endpoint.

# 3. **Access Token**: Ensure that your access token is valid and has not expired. If necessary, refresh the token.

# 4. **Server Status**: Check if the server is running and accessible. If you are running the backend locally, ensure that it is started correctly.

# 5. **Path Parameters**: If the endpoint requires path parameters (like `tripId` or `oAuthProvider`), ensure they are correctly formatted and provided in the request.

# 6. **Logs and Debugging**: Check server logs for any additional error messages that might provide more context on why the resource was not found.

# By following these steps, you should be able to effectively use the API and troubleshoot any 404 errors you encounter."""
# # context = """'package moheng.auth.domain;  import static org.junit.jupiter.api.Assertions.*;  import moheng.auth.infrastructure.KakaoOAuthClient; import org.junit.jupiter.api.DisplayName; import org.junit.jupiter.api.Test; import org.springframework.beans.factory.annotation.Autowired; import org.springframework.boot.test.context.SpringBootTest;  @SpringBootTest public class KakaoOAuthClientTest {     @Autowired     private KakaoOAuthClient kakaoOAuthClient;      @DisplayName("OAuth 클라이언트 식별자가 동일하다면 참을 리턴한다.")     @Test     void OAuth_클라이언트_식별자가_동일하다면_참을_리턴한다() {         // given, when, then         assertTrue(kakaoOAuthClient.isSame("KAKAO"));     } }', 'package moheng.acceptance.fixture;  import io.restassured.RestAssured; import io.restassured.response.ExtractableResponse; import io.restassured.response.Response; import moheng.auth.dto.AccessTokenResponse; import moheng.keyword.dto.KeywordCreateRequest; import moheng.keyword.dto.TripsByKeyWordsRequest; import org.springframework.http.HttpStatus; import org.springframework.http.MediaType;  public class KeywordAcceptenceFixture {      public static ExtractableResponse<Response> 모든_키워드를_찾는다(final AccessTokenResponse accessTokenResponse) {         return RestAssured.given().log().all()                 .auth().oauth2(accessTokenResponse.getAccessToken())                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .when().get("/api/keyword")                 .then().log().all()                 .statusCode(HttpStatus.OK.value())                 .extract();     }      public static ExtractableResponse<Response> 키워드를_생성한다(final String name) {         return RestAssured.given().log().all()                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .body(new KeywordCreateRequest(name))                 .when().post("/api/keyword")                 .then().log().all()                 .statusCode(org.springframework.http.HttpStatus.NO_CONTENT.value())                 .extract();     }      public static ExtractableResponse<Response> 키워드_리스트로_여행지를_추천받는다(final String accessToken, final TripsByKeyWordsRequest tripsByKeyWordsRequest) {         return RestAssured.given().log().all()                 .auth().oauth2(accessToken)                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .body(tripsByKeyWordsRequest)                 .when().post("/api/keyword/trip/recommend")                 .then().log().all()                 .statusCode(HttpStatus.OK.value())                 .extract();     }      public static ExtractableResponse<Response> 랜덤_키워드_리스트로_여행지를_추천받는다() {         return RestAssured.given().log().all()                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .when().get("/api/keyword/random/trip")                 .then().log().all()                 .statusCode(HttpStatus.OK.value())                 .extract();     } }', 'package moheng.acceptance.fixture;  import io.restassured.RestAssured; import io.restassured.response.ExtractableResponse; import io.restassured.response.Response; import moheng.recommendtrip.dto.RecommendTripCreateRequest; import org.springframework.http.HttpStatus; import org.springframework.http.MediaType;  public class RecommendTripAcceptenceFixture {     public static ExtractableResponse<Response> 선호_여행지를_선택한다(final long tripId, final String accessToken) {         return RestAssured.given().log().all()                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .auth().oauth2(accessToken)                 .body(new RecommendTripCreateRequest(tripId))                 .when().post("/api/recommend")                 .then().log().all()                 .statusCode(org.springframework.http.HttpStatus.NO_CONTENT.value())                 .extract();     }      public static ExtractableResponse<Response> AI_맞춤_추천_여행지를_조회한다(final String accessToken) {         return RestAssured.given().log().all()                 .contentType(MediaType.APPLICATION_JSON_VALUE)                 .auth().oauth2(accessToken)                 .when().get("/api/recommend")                 .then().log().all()                 .statusCode(HttpStatus.OK.value())                 .extract();     } }']]

# # [['branch protect test입니다. 젠킨스의 빌드가 성공했을때, 혹은 실패했을 때 머지가 블록되거나 허용되면 성공입니다. 총 두가지로 테스트를 진행합니다.  1. 의도적으로 실패시켜서 머지 블로킹 확인하기 2. 의도적으로 성공시킨후 머지 확인하기', '# Moheng  ## 🖼 Preview ![Preview Image](link_to_your_preview_image)  ## Table of Contents  - [Overview](#-overview) - [Analysis](#-analysis) - [Project Structure](#-project-structure) - [Getting Started](#-getting-started)   - [Prerequisites](#prerequisites)   - [Installation](#installation)   - [Usage](#usage)  ## 📝 Overview 이 프로젝트는 여행 계획 및 추천 시스템을 구축하기 위한 것입니다. - 로젝트의 주요 목적은 사용자에게 맞춤형 여행 추천을 제공하는 것입니다.  ### Main Purpose - 사용자의 선호도와 클릭 데이터를 기반으로 여행지를 추천합니다. - 여행 계획을 세우는 데 도움을 주며, 사용자 경험을 향상시킵니다. - 여행을 좋아하는 사용자들을 주요 대상으로 합니다.  ### Key Features - 소셜 로그인 기능 (Kakao, Google) - 사용자 맞춤형 여행 추천 - 여행 일정 관리 기능 - 실시간 여행 정보 제공  ### Core Technology Stack - Frontend: React, Vite - Backend: Spring Boot - Database: MySQL - 기타: FastAPI, Python  ## 📊 Analysis - 데이터 분석 결과: 사용자 클릭 데이터를 기반으로 한 추천 알고리즘 - 성능 메트릭: 추천의 정확도, 재현율, F1 점수 - 주요 인사이트: 사용자 선호도에 따라 추천의 질이 향상됨  ## 📁 Project Structure ``` moheng ├── 📁 ai │   ├── 📁 model_serving │   │   ├── 📁 application │   │   ├── 📁 domain │   │   ├── 📁 infra │   │   └── 📁 interface │   └── ... ├── 📁 frontend │   ├── 📁 src │   │   ├── 📁 api │   │   ├── 📁 components │   │   └── 📁 pages │   └── ... ├── 📁 backend │   ├── 📁 moheng │   │   ├── 📁 auth │   │   ├── 📁 member │   │   ├── 📁 planner │   │   └── 📁 trip │   └── ... └── ... ```  ## 🚀 Getting Started ### Prerequisites - Docker - Java 22 - Python 3.11 - Node.js  ### Installation ```bash # 레포지토리 클론 git clone https://github.com/kakao-25/moheng.git  # 필요한 패키지 설치 cd frontend npm install  cd ../backend ./gradlew build  cd ../ai pip install poetry poetry install ```  ### Usage ```bash # 프론트엔드 실행 cd frontend npm start  # 백엔드 실행 cd backend ./gradlew bootRun  # AI 모델 실행 cd ai poetry run python main.py ```', '# Moheng  ## 🖼 Preview ![Preview Image](link_to_your_preview_image)  ## Table of Contents  - [Overview](#-overview) - [Analysis](#-analysis) - [Project Structure](#-project-structure) - [Getting Started](#-getting-started)   - [Prerequisites](#prerequisites)   - [Installation](#installation)   - [Usage](#usage)  ## 📝 Overview 이 프로젝트는 여행 계획 및 추천 시스템을 구축하기 위한 것입니다. - 프로젝트의 주요 목적은 사용자에게 맞춤형 여행 추천을 제공하는 것입니다.  ### Main Purpose - 사용자의 선호도와 클릭 데이터를 기반으로 여행지를 추천합니다. - 여행 계획을 세우는 데 도움을 주며, 사용자 경험을 향상시킵니다. - 여행을 좋아하는 사용자들을 주요 대상으로 합니다.  ### Key Features - 소셜 로그인 기능 (Kakao, Google) - 사용자 맞춤형 여행 추천 - 여행 일정 관리 기능 - 실시간 여행 정보 제공  ### Core Technology Stack - Frontend: React, Vite - Backend: Spring Boot - Database: MySQL - 기타: FastAPI, Python  ## 📊 Analysis - 데이터 분석 결과: 사용자 클릭 데이터를 기반으로 한 추천 알고리즘 - 성능 메트릭: 추천의 정확도, 재현율, F1 점수 - 주요 인사이트: 사용자 선호도에 따라 추천의 질이 향상됨  ## 📁 Project Structure ``` moheng ├── 📁 ai │   ├── 📁 model_serving │   │   ├── 📁 application │   │   ├── 📁 domain │   │   ├── 📁 infra │   │   └── 📁 interface │   └── ... ├── 📁 frontend │   ├── 📁 src │   │   ├── 📁 api │   │   ├── 📁 components │   │   └── 📁 pages │   └── ... ├── 📁 backend │   ├── 📁 moheng │   │   ├── 📁 auth │   │   ├── 📁 member │   │   ├── 📁 planner │   │   └── 📁 trip │   └── ... └── ... ```  ## 🚀 Getting Started ### Prerequisites - Docker - Java 22 - Python 3.11 - Node.js  ### Installation ```bash # 레포지토리 클론 git clone https://github.com/kakao-25/moheng.git  # 필요한 패키지 설치 cd frontend npm install  cd ../backend ./gradlew build  cd ../ai pip install poetry poetry install ```  ### Usage ```bash # 프론트엔드 실행 cd frontend npm start  # 백엔드 실행 cd backend ./gradlew bootRun  # AI 모델 실행 cd ai poetry run python main.py ```'"""
# prompt = query_augmentation(query, response)
# print(prompt)
