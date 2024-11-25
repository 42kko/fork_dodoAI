"""문서 처리 관련 코드"""
from dataclasses import dataclass, field
from typing import List, Any, Optional, Set, Dict, Tuple
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import multiprocessing 
import aiohttp
import re
import os
import time
import aiofiles

from ktb_utils import TextProcessor
from ktb_api_client import APIClient
from ktb_prompts import *
from ktb_settings import *
from ktb_func import *
# logger 설정 추가
logger = logging.getLogger(__name__)

@dataclass
class SourceFileInfo:
    """소스 파일의 구조적 정보를 담는 데이터 클래스"""
    package: Optional[str] = None      # 패키지/네임스페이스 (예: com.example.project)
    imports: Set[str] = field(default_factory=set)  # import/using/require 문 집합
    class_name: str = ""              # 클래스/함수명
    content: str = ""                # 파일 전체 내용
    file_type: str = ""             # 파일 타입 (java, py, js 등)
    
    def __post_init__(self):
        """데이터 유효성 검증 및 기본값 설정"""
        if self.imports is None:
            self.imports = set()

        if self.class_name is None:
            self.class_name = ""
            
        if self.content is None:
            self.content = ""
            
        if self.file_type is None:
            self.file_type = ""

    def __str__(self) -> str:
        """사람이 읽기 쉬운 문자열 표현"""
        return (
            f"SourceFileInfo(\n"
            f"  package: {self.package}\n"
            f"  class_name: {self.class_name}\n"
            f"  file_type: {self.file_type}\n"
            f"  imports: {len(self.imports)} items\n"
            f"  content: {len(self.content)} chars\n"
            f")"
        )
    

class DocumentProcessor:
    """문서 생성 및 처리"""
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.text_processor = TextProcessor()
        self.source_extensions = {
            '.java': 'java',
            '.py': 'py',
            '.js': 'js',
            '.ts': 'ts',
            '.cpp': 'cpp',
            '.cs': 'cs'
        }
        self.parsers = {
            'java': self._parse_java_file,
            'py': self._parse_python_file,
            'js': self._parse_javascript_file,
            'ts': self._parse_typescript_file,
            'cpp': self._parse_cpp_file,
            'cs': self._parse_cs_file  
        }
        
    def _parse_source_file(self, content: str, file_type: str) -> SourceFileInfo:
        """소스 파일 파싱"""
        if file_type in self.parsers:
            return self.parsers[file_type](content)
        return self._parse_generic_file(content, file_type)

    def _parse_java_file(self, content: str) -> SourceFileInfo:
        """Java 파일 파싱"""
        imports = set(re.findall(r'^import\s+[\w.*]+;', content, re.MULTILINE))
        package_match = re.search(r'^package\s+([\w.]+);', content, re.MULTILINE)
        class_match = re.search(r'(?:class|interface|enum)\s+(\w+)', content)
        
        package = package_match.group(1) if package_match else None
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=package,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='java'
        )

    def _parse_python_file(self, content: str) -> SourceFileInfo:
        """Python 파일 파싱"""
        imports = set(re.findall(r'^(?:from\s+[\w.]+\s+)?import\s+[\w.*,\s]+', content, re.MULTILINE))
        class_match = re.search(r'(?:class|def)\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=None,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='py'
        )

    def _parse_javascript_file(self, content: str) -> SourceFileInfo:
        """JavaScript 파일 파싱"""
        imports = set(re.findall(r'^(?:import|require)\s+.*?;?$', content, re.MULTILINE))
        class_match = re.search(r'(?:class|function)\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=None,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='js'
        )

    def _parse_typescript_file(self, content: str) -> SourceFileInfo:
        """TypeScript 파일 파싱"""
        imports = set(re.findall(r'^(?:import|require)\s+.*?;?$', content, re.MULTILINE))
        class_match = re.search(r'(?:class|interface|function)\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=None,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='ts'
        )

    def _parse_cpp_file(self, content: str) -> SourceFileInfo:
        """C++ 파일 파싱"""
        imports = set(re.findall(r'#include\s+[<"].*?[>"]', content))
        class_match = re.search(r'(?:class|struct|void|int|bool|char|float|double)\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=None,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='cpp'
        )

    def _parse_cs_file(self, content: str) -> SourceFileInfo:
        """C# 파일 파싱"""
        imports = set(re.findall(r'^using\s+([\w\.]+);', content, re.MULTILINE))
        class_match = re.search(r'(?:class|interface|struct)\s+(\w+)', content)
        class_name = class_match.group(1) if class_match else ""
        
        return SourceFileInfo(
            package=None,
            imports=imports,
            class_name=class_name,
            content=content,
            file_type='cs'
        )

    def _parse_generic_file(self, content: str, file_type: str) -> SourceFileInfo:
        """기본 파서"""
        return SourceFileInfo(
            package=None,
            imports=set(),
            class_name="",
            content=content,
            file_type=file_type
        )
    
    async def process_readme(self, repo_url: str, clone_dir: str, user_name: str, repo_name: str) -> List[Any]:
        """모든 문서 처리 태스크 실행"""
        tasks = []
        
        # README 생성 태스크
        readme_task = asyncio.create_task(
            self._generate_readme(repo_url, clone_dir),
            name="readme_generation"
        )
        tasks.append(readme_task)
        
        # Usage 생성 태스크
        usage_task = asyncio.create_task(
            self._generate_usage(repo_url, clone_dir),
            name="usage_generation"
        )
        tasks.append(usage_task)
        
        # 모든 태스크 실행 및 결과 반환
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            # README와 Usage 병합
            if isinstance(results[0], str) and isinstance(results[1], str):
                merged_content = self._update_readme_with_usage(results[0], results[1])
                await self._save_readme(merged_content, clone_dir, user_name, repo_name)
            
            return results
            
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            raise
    
    async def get_optimized_source_files(self, repo_dir: str) -> Dict[str, List[SourceFileInfo]]:
        """모든 소스 파일 최적화하여 저장"""
        package_map = {}
        source_extensions = {
            '.java': 'java',
            '.py': 'py',
            '.js': 'js',
            '.ts': 'ts',
            '.cpp': 'cpp',
            '.cs': 'cs',
            # 필요한 확장자 추가
        }
        
        for root, _, files in os.walk(repo_dir):
            if any(excl in root for excl in EXCLUDE_DIRS):
                continue
                
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in source_extensions:
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_info = self._parse_source_file(
                            content, 
                            source_extensions[ext]
                        )
                        
                        # 패키지/모듈별로 분류
                        key = file_info.package or os.path.dirname(file_path)
                        if key not in package_map:
                            package_map[key] = []
                        package_map[key].append(file_info)
                        
                except Exception as e:
                    print(f"파일 파싱 오류 ({file_path}): {str(e)}")
        
        return package_map

    
    async def _generate_readme(self, repo_url: str, clone_dir: str) -> Optional[str]:
        """README 생성"""
        try:
            source_files = await self.get_optimized_source_files(clone_dir)
            if not source_files:
                logger.error("소스 파일을 찾을 수 없습니다.")
                return None
            optimized_context = self._build_optimized_context(source_files)
            chunks = self.text_processor.split_text(optimized_context, max_tokens=GPT_MAX_TOKENS)  # 청크 크기 제한
            # 청크 단위로 처리하고 결과 병합
            if len(chunks) > 1:
                result = await self._process_chunks(chunks, repo_url, PROMPT_README_GEMINI)
            else :
                result = await self._process_single_context(chunks[0].text, repo_url, PROMPT_README)
            return result

        except Exception as e:
            logger.error(f"README generation failed: {str(e)}")
            return None

    def _get_build_files(self, repo_dir: str) -> List[str]:
        """빌드 파일 목록 가져오기"""
        build_files = []
        for root, _, files in os.walk(repo_dir):
            if any(excl in root for excl in EXCLUDE_DIRS):
                continue
            
            for file in files:
                if file.endswith(tuple(BUILD_FILE_NAMES)):
                    build_files.append(os.path.join(root, file))
        return build_files

    def _build_files_context(self, build_files: List[str], clone_dir: str) -> str:
        """빌드 파일들의 컨텍스트 구성"""
        context_parts = []
        for file_path in build_files:
            try:
                rel_path = os.path.relpath(file_path, clone_dir)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context_parts.append(
                        f"\n\nFILE_START: {rel_path}\n{content}\nFILE_END\n"
                    )
            except Exception as e:
                logger.error(f"파일 읽기 오류 ({rel_path}): {str(e)}")
                continue
        return "".join(context_parts)

    async def _process_chunks(self, chunks: List[str], repo_url: str, prompt: str) -> Optional[str]:
        """청크 비동기 처리"""
        if MODEL.startswith("gemini"):
            # 세마포어 없이 비동기적으로 청크 처리
            tasks = [
                self.process_chunk(chunk.text, repo_url, prompt) 
                for chunk in chunks
            ]
            chunk_summaries = await asyncio.gather(*tasks)
            chunk_summaries = [s for s in chunk_summaries if s]  # None 값 필터링
        else:
            async with aiohttp.ClientSession() as session:
                chunk_summaries = await self.summarize_chunks_batched(
                    chunks, prompt, session
                )
        if not chunk_summaries:
            return None

        start_time = time.perf_counter()
        messages = [{"role": "system", "content": PROMPT_README_FROM_SUMMARY}]
        for summary in chunk_summaries:
            messages.append({"role": "user", "content": summary})
        messages.append({
            "role": "user", 
            "content": f"Create a readme based on the previous information. git repository url : {repo_url}"
        })
        doc_response, _ = self._get_completion(messages)
        end_time = time.perf_counter()
        print(f"README 생성 완료 처리 시간: {end_time - start_time} 초")
        return doc_response

    async def _process_single_context(self, context: str, repo_url: str, prompt: str) -> Optional[str]:
        """단일 컨텍스트 처리"""
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": context},
            {"role": "user", "content": f"git repo url : {repo_url}"}
        ]
        doc_response, _ = self._get_completion(messages)
        return doc_response

    async def _generate_usage(self, repo_url: str, clone_dir: str) -> Optional[str]:
        """Usage 생성"""
        start_time = time.perf_counter()
        try:
            build_files = self._get_build_files(clone_dir)
            context = self._build_files_context(build_files, clone_dir)
            
            token_count = self.text_processor.count_tokens(context)
            print(f"Total build files: {len(build_files)}, tokens: {token_count}")
            
            if token_count > GPT_MAX_TOKENS:
                chunks = self.text_processor.split_text(context)
                print(f"Split into {len(chunks)} chunks - USAGE")
                result = await self._process_chunks(chunks, repo_url, PROMPT_README)
            else:
                result = await self._process_single_context(context, repo_url, PROMPT_README)

            end_time = time.perf_counter()
            print(f"USAGE 생성 완료 처리 시간: {end_time - start_time} 초")
            return result

        except Exception as e:
            logger.error(f"Usage generation failed: {str(e)}")
            return None

    async def _save_summary_async(self, category: str, filename: str, summary: str, 
                                output_directory: str, io_pool: ThreadPoolExecutor):
        """비동기로 파일 저장"""
        if not summary:
            return
            
        category_dir = os.path.join(output_directory, category)
        os.makedirs(category_dir, exist_ok=True)
        
        output_file_name = os.path.join(
            category_dir,
            self._extract_filename(filename).replace('.java', '.md')
        )

        # 파일명이 중복될 경우 처리
        base_name, extension = os.path.splitext(output_file_name)
        counter = 1
        while os.path.exists(output_file_name):
            output_file_name = f"{base_name}_{counter}{extension}"
            counter += 1

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            io_pool,
            lambda: open(output_file_name, "w", encoding="utf-8").write(remove_markdown_blocks(summary))
        )

    def _get_code_contents(self, files: List[str]) -> List[str]:
        """파일 내용 읽기"""
        contents = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    contents.append(f.read())
            except Exception as e:
                logger.error(f"파일 읽기 오류 ({file}): {str(e)}")
                contents.append("")
        return contents

    def _extract_filename(self, filepath: str) -> str:
        """파일 경로에서 파일명 추출"""
        return os.path.basename(filepath)

    def _build_optimized_context(self, package_map: Dict[str, List[SourceFileInfo]]) -> str:
        """최적화된 컨텍스트 생성"""
        context_parts = []
        
        for package, classes in package_map.items():
            # 패키지별로 공통 import문 처리
            common_imports = set.intersection(*[cls.imports for cls in classes])
            
            context_parts.append(f"\nPACKAGE: {package}")
            if common_imports:
                context_parts.append("COMMON IMPORTS:")
                context_parts.extend(sorted(common_imports))
            
            # 각 클래스의 고유한 내용만 포함
            for cls in classes:
                unique_imports = cls.imports - common_imports
                class_context = [
                    f"\nCLASS: {cls.class_name}",
                    "UNIQUE IMPORTS:" if unique_imports else "",
                    "\n".join(sorted(unique_imports)),
                    cls.content
                ]
                context_parts.append("\n".join(filter(None, class_context)))
        
        return "\n".join(context_parts)
    
    def _get_completion(
        self,  # self 매개변수 추가
        messages: List[Dict],
        model: Optional[str] = MODEL,
        temperature: Optional[float] = TEMPERATURE,
        stop: Optional[List[str]] = None,
        tools: Optional[List] = None,
        logprobs: Optional[int] = None,
        top_logprobs: Optional[Dict[str, float]] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = False,
    ) -> Tuple[str, Any]:
        params = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        if tools:
            params["tools"] = tools

        try:
            if MODEL.startswith("claude"):
                params["max_tokens"] = max_tokens
                params["stop_sequences"] = stop
                params["seed"] = SEED

                completion = client_claude.messages.create(**params)
                return completion.content[0].text, None  # 텍스트만 반환
            
            else:
                params["model"] = "GPT_MODEL"
                params["stop"] = stop
                params["logprobs"] = logprobs
                params["top_logprobs"] = top_logprobs
                params["seed"] = SEED

                completion = client_gpt.chat.completions.create(**params)
                return completion.choices[0].message.content, None  # 텍스트만 반환
                
        except Exception as e:
            logger.error(f"Completion 생성 오류: {str(e)}")
            return "", None

    def _update_readme_with_usage(self, readme_content: str, usage_content: str) -> str:
        try:
            # usage_content에서 Getting Started 이후 내용만 추출
            usage_match = re.search(r"## 🚀 Getting Started\n([\s\S]*$)", usage_content)
            if usage_match:
                usage_after_started = usage_match.group(1)  # Getting Started 이후 내용만 가져오기
                
                # readme_content에서 Getting Started 이후 내용 교체
                pattern = r"(## 🚀 Getting Started\n)([\s\S]*$)"
                new_content = re.sub(pattern, 
                                r"\1" + usage_after_started,
                                readme_content)
                print("README가 성공적으로 업데이트 되었습니다.")

                return remove_markdown_blocks(new_content)
        except Exception as e:
            print(f"오류 발생: {e}")
        return readme_content  # 실패 시 원본 환

    async def _save_readme(self, content: str, clone_dir: str, user_name: str, repo_name: str):
        """README 파일 저장"""
        readme_path = os.path.join(clone_dir, "README.md")

        try:
            async with aiofiles.open(readme_path, "w", encoding="utf-8") as f:
                await f.write(content)
            print(f"README가 저장되었습니다: {readme_path}")
            await upload_to_s3(BUCKET_NAME, readme_path, f"{user_name}_{repo_name}_README.md")
        except Exception as e:
            logger.error(f"README 저장 중 오류: {str(e)}")

    async def summarize_chunks_batched(self, chunks, summary_prompt, session):
        """청크 배치 처리"""
        return await self.api_client.process_chunks(chunks, summary_prompt)

    async def generate_text_async(self, session, prompt, contents):
        """비동기 텍스트 생성"""
        return await self.api_client.generate_text(session, prompt, contents)

    async def process_chunk(self, chunk: str, repo_url: str, prompt: str) -> Optional[str]:
        """단일 청크 처리"""
        try:
            start_time = time.perf_counter()
            model = genai.GenerativeModel(
                model_name=MODEL,
                system_instruction=prompt,
            )
            chat = model.start_chat(
                history=[
                    {"role": "user", "parts": prompt}
                ]
            )
            
            # 비동기적으로 메시지 전송
            response = await asyncio.to_thread(
                chat.send_message,
                f"git repository url : {repo_url}\n\n" + chunk
            )
            end_time = time.perf_counter()
            print(f"### 파트 요약 완료 처리 시간: {end_time - start_time} 초")
            return response.text
            
        except Exception as e:
            print(f"청크 처리 중 오류: {str(e)}")
            return None

    async def generate_docs(self, directory_path: dict[str, list], output_directory: str, include_test: bool):
        """문서만 생성"""
        try:
            io_pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 2)
            
            # 카테고리별 프롬프트 정의
            prompts = {
                'Service': SERVICE_DOC_PROMPT,
                'Controller': CONTROLLER_DOC_PROMPT,
                'RestController': CONTROLLER_DOC_PROMPT,
                'Test': TEST_DOC_PROMPT
            }
            
            all_tasks = []
            for category, files in directory_path.items():
                code_contents = self._get_code_contents(files)
                all_tasks.extend([
                    (category, filename, content)
                    for filename, content in zip(files, code_contents)
                ])
            
            chunk_size = 50
            async with aiohttp.ClientSession() as session:
                for i in range(0, len(all_tasks), chunk_size):
                    chunk = all_tasks[i:i + chunk_size]
                    
                    tasks = [
                        self.api_client.generate_text(session, prompts[category], content) 
                        for category, _, content in chunk
                    ]
                    summaries = await asyncio.gather(*tasks)
                    
                    save_tasks = [
                        self._save_summary_async(category, filename, summary, output_directory, io_pool)
                        for (category, filename, _), summary in zip(chunk, summaries)
                    ]
                    await asyncio.gather(*save_tasks)

            return output_directory

        except Exception as e:
            logger.error(f"문서 생성 실패: {str(e)}")
            return None
        finally:
            io_pool.shutdown()
    
    def categorize_files(self, directory, include_test=INCLUDE_TEST):
        """각 카테고리 폴더(Service, Controller, Test) 내의 파일들을 분류"""
        categories = {
            "Service": [],
            "Controller": []  # Controller와 RestController를 함께 처리
        }
        
        # Test 파일을 포함할지 여부에 따라 카테고리 추가
        if include_test:
            categories["Test"] = []

        # 각 카테고리 폴더 확인
        for category in ["Service", "Controller", "RestController", "Test"]:
            if category == "Test" and not include_test:
                continue  # Test 파일을 포함하지 않으면 건너뜁니다

            category_path = os.path.join(directory, category)
            if os.path.exists(category_path):
                for filename in os.listdir(category_path):
                    if filename.endswith(".md"):
                        # Controller와 RestController를 같은 카테고리에 추가
                        if category in ["Controller", "RestController"]:
                            categories["Controller"].append(filename)
                        elif category == "Test" and include_test:
                            categories["Test"].append(filename)
                        else:
                            categories[category].append(filename)
        
        return categories

    async def summarize_docs_async(self, directory, include_test):
        category_files = self.categorize_files(directory, include_test)
        summaries = {"Service": {}, "Controller": {}, "Test": {}}
        
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    self.summarize_category,
                    files, category, directory
                )
                for category, files in category_files.items()
            ]
            
            results = await asyncio.gather(*tasks)

            # 결과를 summaries에 저장
            for category, result in zip(category_files.keys(), results):
                if result:  # 빈 결과는 건너뛰기
                    summaries[category] = result

        # 요약이 있는 카테고리만 파일 생성
        for category, summary_dict in summaries.items():
            if not summary_dict:  # 빈 딕셔너리 건너뛰기
                continue
                
            output_path = os.path.join(directory, f"{category}_summary.md")
            
            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                await f.write(f"# {category} Files Summary\n\n")
                for filename, summary in summary_dict.items():
                    if summary is not None:
                        await f.write(f"## {filename}\n{remove_markdown_blocks(summary)}\n\n")
            
            print(f"{output_path} file created successfully.")
        
        return None

    def summarize_category(self, files, category, directory):
    # 각 프로세스에서 별도의 aiohttp.ClientSession 생성
        async def run():
            async with aiohttp.ClientSession() as session:
                return await self.summarize_docs(files, os.path.join(directory, category), session)
        
        return asyncio.run(run())
    
    async def summarize_docs(self, files, directory, session):
        if not files:  # 빈 리스트 체크
            print(f"No {directory} provided to process")
            return {}
        tasks = []
        
        for filename in files:
            # 전체 파일 경로 구성
            file_path = os.path.join(directory, filename)
            
            try:        
                # 파일이 실제로 존재하고 디렉토리가 아닌지 확인
                if not os.path.isfile(file_path):
                    print(f"Skipping directory or non-existent file: {file_path}")
                    continue

                async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
                    text = await file.read()
                    tasks.append((filename, self.generate_text_async(session, SUMMARY_PROMPT, text)))
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue
        
        if not tasks:
            print(f"No valid files found in directory: {directory}")
            return {}
        
        try:
            # Run tasks and gather results
            results = await asyncio.gather(*[task[1] for task in tasks])
            # Build summaries dictionary for the category
            summaries = {tasks[i][0]: results[i] for i in range(len(tasks)) if results[i] is not None}
            return summaries
        except Exception as e:
            print(f"Error processing tasks: {e}")
            return {}

    async def process_chunk(self, chunk: str, repo_url: str, prompt: str) -> Optional[str]:
        """단일 청크 처리"""
        try:
            start_time = time.perf_counter()
            model = genai.GenerativeModel(
                model_name=MODEL,
                system_instruction=prompt,
            )
            chat = model.start_chat(
                history=[
                    {"role": "user", "parts": prompt}
                ]
            )
            
            # 비동기적으로 메시지 전송
            response = await asyncio.to_thread(
                chat.send_message,
                f"git repository url : {repo_url}\n\n" + chunk
            )
            end_time = time.perf_counter()
            print(f"### 파트 요약 완료 처리 시간: {end_time - start_time} 초")
            return response.text
            
        except Exception as e:
            print(f"청크 처리 중 오류: {str(e)}")
            return None