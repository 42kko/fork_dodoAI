from openai import OpenAI
from langchain_text_splitters import MarkdownHeaderTextSplitter
import anthropic
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import boto3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from autotiktokenizer import AutoTikTokenizer
from token_chunker import TokenChunker
# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY') 
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# 필수 환경 변수 확인
required_vars = [
    'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'GEMINI_API_KEY'
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Required environment variable {var} is not set")
    

"""**PARAMETER SETTINGS**"""
#모델 설정
MODEL = 'gemini-1.5-flash'
GPT_MODEL = 'gpt-4o-mini'
TEMPERATURE = 0.1
SEED = 213
TOP_LOGPROBS = 5 #logprob token 개수

if MODEL.startswith('gpt' or 'claude'):
    MAX_TOKENS_PER_BATCH = 1500000
    MAX_TOKEN_LENGTH = 120000
elif MODEL.startswith('gemini'):
    MAX_TOKENS_PER_BATCH = 3500000
    MAX_TOKEN_LENGTH = 1000000
    genai.configure(api_key=GEMINI_API_KEY)

tokenizer = AutoTikTokenizer.from_pretrained("gpt2")
chunker = TokenChunker(
        tokenizer=tokenizer,
        chunk_size=MAX_TOKEN_LENGTH,  # maximum tokens per chunk
        chunk_overlap=128  # overlap between chunks
    )
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIM = 1536
DISTANCE = {"hnsw:space": "cosine"}
GPT_MAX_TOKENS = 120000
headers_to_split_on = [
    (
        "#",
        "Header 1",
    ),
    (
        "##",
        "Header 2",
    ),
    (
        "###",
        "Header 3",
    )
]
FILE_EXTENSIONS = [
    '.py', '.pyw', '.pyc', '.pyo',  # Python
    '.java', '.class',     # Java
    '.c', '.h',                     # C
    '.cpp', '.hpp', '.cc', '.cxx',  # C++
    '.js', '.mjs',                  # JavaScript
    '.html', '.htm',                # HTML
    '.css',                         # CSS
    '.rb',                          # Ruby
    '.php',                         # PHP
    '.swift',                       # Swift
    '.go',                          # Go
    '.rs',                          # Rust
    '.kt', '.kts',                 # Kotlin
    '.R', '.r', '.Rmd',            # R
    '.scala',                       # Scala
    '.pl', '.pm',                  # Perl
    '.ts', '.tsx',                 # TypeScript
    '.sh', '.bash',                # Shell Script
    '.sql',                        # SQL
    '.md'                           # Markdown
]
EXCLUDE_DIRS = ['.git', 'node_modules', 'venv', '__pycache__', 'dist', 'tests', 'test', 'examples', 'example', '.DS_Store', 'gradle-wrapper','__MACOSX']
BUILD_FILE_NAMES = [
    'Makefile', 'CMakeLists.txt', 'setup.py', 'main.py', 'pyproject.toml',
    'config.js', 'go.mod', 'Cargo.toml', 'Gemfile', 'pom.xml', 'package.json',
    '.env', 'Dockerfile', 'gradle', 'requirements.txt', 'build',
    'setup.cfg', 'requirements-dev.txt', 'tox.ini', 'configure.ac', 'config.h.in',
    '.csproj', '.sln', 'tsconfig.json', 'webpack.config.js', 'gulpfile.js',
    'rollup.config.js', 'build.gradle', 'settings.gradle', 'Jenkinsfile',
    'Vagrantfile', 'Procfile', 'Brewfile', '.md'
]
SRC_FILE_NAMES = ['.py', '.js', '.ts', '.java', '.cpp', '.h', '.hpp', '.cs', '.go', '.rs', '.rb', '.php']

MAX_RETRIES = 2 # 최대 재시도 횟수
RETRY_DELAY = 3 # 재시도 간격 (초)
INCLUDE_TEST = False

client_claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
client_gpt = OpenAI(api_key=OPENAI_API_KEY)
client_gemini = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
# 환경 변수로 실행 환경 확인
IS_DOCKER = os.getenv('IS_DOCKER', 'false').lower() == 'true'

# 환경에 따른 경로 설정
if IS_DOCKER:
    CHROMA_PATH = "/app/chroma_data"  # Docker 환경
else:
    CHROMA_PATH = "./chroma_data"     # 로컬 환경

# ChromaDB 클라이언트 초기화
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on,strip_headers=False)
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name=EMBEDDING_MODEL)

# S3 클라이언트 생성
s3 = boto3.client(
	's3',
	aws_access_key_id=AWS_ACCESS_KEY_ID,
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
BUCKET_NAME = 'haon-dododocs'