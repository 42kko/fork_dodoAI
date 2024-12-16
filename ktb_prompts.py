"""**PROMPTS**"""
SUMMARY_PROMPT = """Please provide a concise summary of the provided documentation, focusing on:

1. Component Overview
- Main responsibilities and purposes
- Key features and capabilities
- Core patterns and approaches used

2. Architecture & Implementation
- Major components and their roles
- Component interactions and dependencies
- Key implementation patterns
- Critical flows and processes

Please keep the summary clear and organized with bullet points where appropriate. Focus on high-level architectural patterns and main concepts without implementation details.

Note: Examples of generated summaries will look like:

For Services:
- Core business logic and domain operations
- Service interaction patterns
- Transaction management approaches
- Business error handling strategies

For Controllers:
- API endpoints and capabilities
- Request/response handling patterns
- Controller organization patterns
- API error handling approaches

For Tests:
- Test coverage and strategies
- Test organization patterns
- Documentation testing approaches
- Key test scenarios
"""

# CHATBOT_PROMPT = """You are a helpful assistant.

# When answering:
# 1. Only use information from the provided context and chat history
# 2. If the context is relevant but insufficient to fully answer the query, use information from the chat history
# 3. If you're unsure about the relevance of the context, explain why
# 4. Never make up information that's not in the context

# Remember to:
# - User Intruction is more important than context
# - Be concise and direct
# - Cite specific parts of the context when relevant
# - Use the code provided to provide a code-included answer
# - Maintain a helpful and professional tone"""

CHATBOT_PROMPT = """You are a precise code-based QA assistant with context-driven response generation.

Language Response Rule:
- ALWAYS respond in the EXACT SAME LANGUAGE as the user's query
- Maintain full technical precision while using the user's language

Code Reference Guidelines:
- MANDATORY: Include actual code implementations for key concepts discussed
- When explaining a concept, directly attach:
 1. The exact code snippet that implements the concept
 2. Full file path and location of the code
 3. Relevant line numbers or code block markers
- If multiple code implementations exist, prioritize the most relevant or detailed one

Context Processing Rules:
- Mandatory Reference: Always cite the specific file(s) and location(s) from which information is sourced
- Source Transparency: Include full file path/name when referencing context
- Code Citation: When discussing code, directly quote or reference exact code snippets from the provided context
- NEVER generate arbitrary code not present in the context

Response Structure:
1. Conceptual Explanation
2. Code Implementation Reference
  - File Name
  - Full File Path
  - Exact Code Snippet
  - Explanation of Code's Relevance

Additional Guidelines:
- Prioritize showing actual implementation over abstract explanations
- Ensure code snippets directly illustrate the discussed concept
- Provide context for why this specific code is relevant

Strict Compliance:
- Zero tolerance for information fabrication
- Complete traceability of information sources
- Transparent about context limitations
- Always prefer showing actual code over theoretical descriptions"""

DALLE_PROMPT = '''
Draw the core features clearly. 
A simple vector logo for project.
project : '''

SUMMARY_PROMPT_KOREAN = """Please provide a concise summary of the provided documentation, focusing on:

1. Component Overview
- Main responsibilities and purposes
- Key features and capabilities
- Core patterns and approaches used

2. Architecture & Implementation
- Major components and their roles
- Component interactions and dependencies
- Key implementation patterns
- Critical flows and processes

Please keep the summary clear and organized with bullet points where appropriate. Focus on high-level architectural patterns and main concepts without implementation details.

Note: Examples of generated summaries will look like:

For Services:
- Core business logic and domain operations
- Service interaction patterns
- Transaction management approaches
- Business error handling strategies

For Controllers:
- API endpoints and capabilities
- Request/response handling patterns
- Controller organization patterns
- API error handling approaches

For Tests:
- Test coverage and strategies
- Test organization patterns
- Documentation testing approaches
- Key test scenarios

MUST reponse in Korean.
"""

NEW_PROMPT_TEST_DOC = '''
Analyze the following test file and generate a test document in Markdown format:

# [Test File Content]

## Test Overview
- **Test Target**: `TestedClass`
- **Test Environment**:
  - Environment Configuration 1
  - Environment Configuration 2

## Test Cases

### `testMethod()`
#### Scenario
- Test Purpose
- Test Conditions

#### Test Data
```json
{
    "Test Input Data"
}
```

#### Expected Result
```json
{
    "Expected Output Data"
}
```

#### Verification Points
- [ ] Verification Item 1
- [ ] Verification Item 2

Instructions for Document Creation:

1. Clearly explain the purpose of all test methods.
2. Describe the test data and expected results in detail.
3. Specify the test execution conditions or constraints.
4. Must response in English.
'''

NEW_PROMPT_TEST_DOC_KOREAN = '''
다음 테스트 파일을 분석하여 마크다운 형식의 테스트 문서를 생성해주세요:

# [Test 파일 내용]

## 테스트 개요
- **테스트 대상**: `TestedClass`
- **테스트 환경**:
  - 환경 구성 1
  - 환경 구성 2

## 테스트 케이스

### `testMethod()`
#### 시나리오
- 테스트 목적
- 테스트 조건

#### 테스트 데이터
```json
{
    "테스트 입력 데이터"
}
```

#### 예상 결과
```json
{
    "예상 출력 데이터"
}
```

#### 검증 포인트
- [ ] 검증 항목 1
- [ ] 검증 항목 2


문서 작성 시 주의사항:
1. 모든 테스트 메서드의 목적을 명확히 설명하세요
2. 테스트 데이터와 예상 결과를 구체적으로 기술하세요
3. 테스트 실행 조건이나 제약사항을 명시하세요
'''


NEW_PROMPT_ARCHITECTURE_DOC = '''
Instructions for Document Creation:

1. Repeat the above format for all API endpoints.
2. Include actual request/response examples.
3. Document all possible response status codes.
4. Clearly specify if authentication or authorization is required.
5. Clearly express the overall structure of the system.
6. Explain the roles and responsibilities of each component.
7. Represent the main data flow using a sequence diagram.
8. Must response in English.

Analyze the provided code and generate an architecture document in Markdown and Mermaid format:

# System Architecture

## Overall Structure

```mermaid
graph TD
    A[Client] --> B[Controller Layer]
    B --> C[Service Layer]
    C --> D[Repository Layer]
    D --> E[Database]
```

## System Flow

```mermaid
sequenceDiagram
    Client->>Controller: Request
    Controller->>Service: Process
    Service->>Repository: Data Access
    Repository->>Database: Query
```

## Description of Main Components

### Controller Layer

*   Roles and Responsibilities
*   List of Main Controllers
*   Common Processing Logic

### Service Layer

*   Business Logic Structure
*   List of Main Services
*   Transaction Boundaries

---

# [API Name]

## Overview

*   Controller Description
*   Base URL Path
*   Common Request/Response Format

## API Endpoints

### [API Name]

**[HTTP Method]** `/api/path`

#### Description

[API Function Description]

#### Request

##### Parameters

| Name   | Type   | Required | Description |
| ------ | ------ | -------- | ----------- |
| param1 | string | Required | Description |

##### Headers

| Name          | Required | Description       |
| ------------- | -------- | ----------------- |
| Authorization | Required | Bearer {token} |

##### Request Body

```json
{
    "Example Request Body"
}
```

#### Response

##### Success Response

*   Status: 200 OK

```json
{
    "Example Response Body"
}
```

##### Error Response

*   Status: 400 Bad Request

```json
{
    "error": "Error Message"
}
```
'''


NEW_PROMPT_ARCHITECTURE_DOC_KOREAN = '''
문서 작성 시 주의사항:
1. 모든 API 엔드포인트에 대해 위 형식을 반복해서 작성하세요
2. 실제 요청/응답 예시를 포함하세요
3. 가능한 모든 응답 상태 코드를 문서화하세요
4. 인증이나 권한이 필요한 경우 반드시 명시하세요
5. 시스템의 전체적인 구조를 명확히 표현하세요
6. 각 컴포넌트의 역할과 책임을 설명하세요
7. 주요 데이터 흐름을 시퀀스 다이어그램으로 표현하세요

제공된 코드를 분석하여 마크다운과 Mermaid 형식의 아키텍처 문서를 생성해주세요:
# 시스템 아키텍처

## 전체 구조
```mermaid
graph TD
    A[Client] --> B[Controller Layer]
    B --> C[Service Layer]
    C --> D[Repository Layer]
    D --> E[Database]
```

## 시스템 흐름
```mermaid
sequenceDiagram
    Client->>Controller: Request
    Controller->>Service: Process
    Service->>Repository: Data Access
    Repository->>Database: Query
```

## 주요 컴포넌트 설명
### Controller Layer
- 역할과 책임
- 주요 컨트롤러 목록
- 공통 처리 로직

### Service Layer
- 비즈니스 로직 구조
- 주요 서비스 목록
- 트랜잭션 경계

--------------------------------

# [API 이름]

## 개요
- 컨트롤러 설명
- 기본 URL 경로
- 공통 요청/응답 형식

## API 엔드포인트

### [API 이름]
**[HTTP Method]** `/api/path`

#### 설명
[API 기능 설명]

#### 요청
##### Parameters
| 이름 | 타입 | 필수 여부 | 설명 |
|------|------|-----------|------|
| param1 | string | Required | 설명 |

##### Headers
| 이름 | 필수 여부 | 설명 |
|------|-----------|------|
| Authorization | Required | Bearer {token} |

##### Request Body
```json
{
    "예시 요청 본문"
}
```

#### 응답
##### Success Response
- Status: 200 OK
```json
{
    "예시 응답 본문"
}
```

##### Error Response
- Status: 400 Bad Request
```json
{
    "error": "에러 메시지"
}
```
'''

AUGMENTATION_PROMPT = """You are an advanced AI system designed to generate optimized vector database search queries from user input. Your task is to analyze technical questions and convert them into efficient, precise queries that will yield the most relevant results from a vector database.

Please follow these steps to generate the optimized query:

1. Analyze the user's input:
   - Identify primary technologies mentioned
   - Extract specific technical challenges or problems
   - Note any particular frameworks, methods, or APIs referenced

2. Process the input:
   - Remove any redundant or unnecessary information
   - Standardize technical terminology for consistency
   - Focus on the most actionable technical context

3. Extract keywords:
   - Identify critical technical keywords
   - Prioritize terms related to core technologies, frameworks, and methods
   - Include specific technical terms, libraries, and APIs
   - Ensure keywords are precise and searchable

4. Generate a contextual sentence:
   - Create a concise, meaningful sentence that captures the essence of the technical problem
   - Balance technical specificity with clarity
   - Provide minimal context for semantic understanding

5. Compose the query:
   - Combine the extracted keywords with the contextual sentence
   - Limit the query to 10-15 words
   - Avoid unnecessary articles and filler words
   - Maintain technical precision

6. Format the output:
   - Use a colon-separated format
   - Structure: [Core Keywords]: [Contextual Description]

Output structure (purely for format, not content):  core keywords: specific technical problem description
"""

# Modular README Blocks
OVERVIEW_BLOCK = """
## 📝 Overview
[Brief overview of the project]
- Main purpose of the project

### Main Purpose
- [Describe the primary goal and purpose of your project]
- [Explain what problem it solves]
- [Mention target users/audience]

### Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

### Core Technology Stack
-Skip sections if no relevant technology is used.
-if you need to make sections, you can make sections like this:
- Frontend: [e.g., React, Vue, Angular]
- Backend: [e.g., Node.js, Python, Java]
- Database: [e.g., PostgreSQL, MongoDB]
- Others(AI, Model, etc.): [e.g., Python, Java]
"""

STRUCTURE_BLOCK = """
## 📁 Project Structure
-don't have expose all files, expose important files/folders with Key Features 

[project name]
├── 📁 [folder1]
│   ├── [folder/file]
│   └── ...
├── 📁 [folder2]
│   ├── [folder/file]
│   ├── [folder/file]
│   └── ...
└── ...
"""

START_BLOCK = """
## 🚀 Getting Started
### Prerequisites
- Supported Operating Systems
  * [List compatible OS: Windows, macOS, Linux]
- Required Software
  * [Runtime environment: Node.js, Python, Java, etc.]
  * [Version requirements]
  * [Package managers: npm, pip, etc.]
- System Dependencies
  * [Any system-level libraries or tools]

### Installation
- If you have Dockerfile, you can use it.
- Include all installation methods in Dockerfiles
- 
```bash
# Clone the repository
git clone [repository-url]
cd [project-name]

# Install required packages
[installation commands]
-If your project has multiple components (e.g., frontend, backend, database, ai) :
  * [Frontend Setup]
  * [Backend Setup]
  * [Database Setup]
  * [AI/Services Setup]

# Configure environments
[configuration commands]
```

### Usage
bash
# How to run
[execution commands]
"""


MOTIVATION_BLOCK = """
## 💡 Motivation
- What inspired this project?
- What problem does it solve?
- Personal or professional context
"""

DEMO_BLOCK = """
## 🎬 Demo
![Demo Video or Screenshot](path/to/demo.mp4)
"""

DEPLOYMENT_BLOCK = """
## 🌐 Deployment
- Deployment platforms (Heroku, AWS, etc.)
- Deployment steps
- Environment-specific configurations
"""

CONTRIBUTORS_BLOCK = """
## 🤝 Contributing
- How to contribute
- Coding standards
- Pull request process
- Code of conduct
"""

FAQ_BLOCK = """
## ❓ Troubleshooting & FAQ
- Common issues
- Frequently asked questions
- Debugging tips
"""

PERFORMANCE_BLOCK = """
## 📈 Performance
- Benchmarks
- Optimization techniques
- Scalability considerations
"""

# 블록들 정의
README_BLOCKS = {
    "OVERVIEW_BLOCK": OVERVIEW_BLOCK,
    "STRUCTURE_BLOCK": STRUCTURE_BLOCK,
    "START_BLOCK": START_BLOCK,
    "MOTIVATION_BLOCK": MOTIVATION_BLOCK,
    "DEMO_BLOCK": DEMO_BLOCK,
    "DEPLOYMENT_BLOCK": DEPLOYMENT_BLOCK,
    "CONTRIBUTORS_BLOCK": CONTRIBUTORS_BLOCK,
    "FAQ_BLOCK": FAQ_BLOCK,
    "PERFORMANCE_BLOCK": PERFORMANCE_BLOCK,
}


def generate_ordered_readme_template(ordered_blocks):
    """
    Generate a README template based on the input order of selected blocks.

    Parameters:
    - project_name (str): The name of the project.
    - ordered_blocks (list): List of tuples (block_name, block_content) in the desired order.

    Returns:
    - str: The formatted README template.
    """

    table_of_contents = []
    readme_content = f"# Project Name\n\n"

    # Table of Contents header
    readme_content += "## Table of Contents\n\n"

    # Process blocks in input order
    for block_name in ordered_blocks:
        block_content = README_BLOCKS[block_name]
        section_title = block_content.split("\n")[1].strip("# ").strip()
        anchor_link = section_title.lower().replace(" ", "-")
        table_of_contents.append(f"[ {section_title}](#{anchor_link})")
        readme_content += block_content + "\n"

    # Add Table of Contents
    readme_content = (
        readme_content.replace("## Table of Contents\n\n",
                               "## Table of Contents\n\n" + "\n".join(table_of_contents) + "\n\n")
    )
    return readme_content


def generate_readme_prompt(blocks, korean=False):
    readme_template = generate_ordered_readme_template(blocks)
    template = f"""Please analyze the entire repository structure and generate a README.md in the following format:

{readme_template}
"""
    if korean:
        template += "Do not generate other contents. MUST fill only the sections that are provided.\nMUST reponse all readme and annotations in Korean. except for the code and Project Name."
    else:
        template += "Do not generate other contents. MUST fill only the sections that are provided.\nMUST reponse all readme and annotations in English. except for the code and Project Name."
    return template


print(generate_readme_prompt(['OVERVIEW_BLOCK', 'STRUCTURE_BLOCK', 'START_BLOCK', 'MOTIVATION_BLOCK',
      'DEMO_BLOCK', 'DEPLOYMENT_BLOCK', 'CONTRIBUTORS_BLOCK', 'FAQ_BLOCK', 'PERFORMANCE_BLOCK'], korean=True))
