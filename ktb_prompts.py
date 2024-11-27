"""**PROMPTS**"""
SERVICE_DOC_PROMPT = '''Please provide comprehensive documentation for the given Spring Service code, following these guidelines:

1. Service Overview
- Begin with a high-level overview of the Service's purpose and responsibilities
- Document the main business operations provided
- List all public methods exposed by the service
- Describe transaction requirements
- Document common error scenarios and handling approaches

2. Business Logic Handling
- Document each public method including:
  * Method signature and purpose
  * Input parameters and validation rules
  * Expected return values
  * Transaction boundaries and isolation levels
  * Business rules and validation logic
  * Error scenarios and handling strategies
  * Code examples of usage

3. Detailed Component Documentation
For each component, provide:

a. Service Class:
- Class name and business purpose
- Dependency injections and autowired components
- Transaction management configuration
- Exception handling strategies
- Validation approaches

b. Business DTOs:
- Field descriptions and validation constraints
- Data transformation/mapping logic
- Domain model relationships

4. Integration Points
- Document interactions with:
  * Repositories and database operations
  * Other services
  * External systems (if applicable)
  * Event publishing/handling (if applicable)

5. Implementation Flow
Include diagrams showing:
- Business logic processing pipeline
- Service-Repository interaction
- Error handling flow
- Transaction boundaries

Include Mermaid diagrams for:
1. Component diagram showing service dependencies
2. Sequence diagram showing business logic flow
3. State diagram for complex operations (if applicable)

6. Testing Considerations
- Document key test scenarios
- Describe mocking requirements
- List critical business edge cases to consider

Remember to use clear, concise language and provide context where necessary. Include common usage examples with code snippets for each business method. Response documentation only. Use markdown format.
'''

CONTROLLER_DOC_PROMPT = '''Please provide comprehensive documentation for the given Spring Controller code, following these guidelines:

1. Controller Overview
- Begin with a high-level overview of the Controller's purpose and responsibilities
- Document the base URL path and any common request mappings
- List all REST endpoints exposed by the controller
- Describe authentication/authorization requirements
- Document common response formats and status codes

2. Request Handling
- Document each @RequestMapping method including:
  * HTTP method (GET, POST, etc.)
  * URL path and parameters
  * Request body format (if applicable)
  * Required headers or cookies
  * Expected response format
  * Possible response status codes and their meanings
  * Error handling and validation

3. Detailed Component Documentation
For each component, provide:

a. Controller Class:
- Class name and purpose
- Dependency injections and autowired components
- Cross-cutting concerns (logging, validation, etc.)
- Security annotations and access control
- Exception handling strategies

b. Request/Response DTOs:
- Field descriptions and validation constraints
- Data transformation/mapping logic
- Serialization/deserialization details

4. Integration Points
- Document interactions with:
  * Services and repositories
  * External APIs or systems
  * Message queues or events
  * Caching mechanisms

5. Implementation Flow
Include diagrams showing:
- Request processing pipeline
- Controller-Service-Repository interaction
- Error handling flow
- Authentication/Authorization flow

Include Mermaid diagrams for:
1. Component diagram showing controller dependencies
2. Sequence diagram showing request processing flow
3. State diagram for complex operations (if applicable)

6. Testing Considerations
- Document key test scenarios
- Describe mocking requirements
- List critical edge cases to consider

Remember to use clear, concise language and provide context where necessary. Include common usage examples and curl commands for API endpoints. Response documentation only. Use markdown format.
'''

TEST_DOC_PROMPT = '''Please provide comprehensive documentation for the given Spring Test code, following these guidelines:

1. Test Suite Overview
- Describe the scope and purpose of the test suite
- Document test categories (unit, integration, e2e)
- List key testing frameworks and tools used (JUnit, REST Docs, etc.)
- Explain test configuration and setup

2. API Documentation Tests
- Document REST Docs test configuration
- Detail API documentation generation process
- For each API endpoint test:
  * HTTP request specifications
    - Method, path, parameters
    - Headers and authentication
    - Request body structure
    - Example request payloads
  * HTTP response specifications
    - Status codes and their meanings
    - Response headers
    - Response body structure
    - Example response payloads
  * Validation constraints
  * Error scenarios and responses

3. Test Environment
- Document required configuration properties
- Describe test database setup
- Detail mock services and test doubles
- Explain test data preparation
- Document required Spring profiles

4. Test Categories
For each test category, document:

a. Unit Tests:
- Test class structure and naming conventions
- Mocking strategies and tools
- Common test utilities and helpers
- Test lifecycle management

b. Integration Tests:
- Test container configuration
- Database initialization scripts
- External service mocks
- Security configuration for tests
- API contract validation tests

c. End-to-End Tests:
- Test environment setup
- Data seeding approach
- Cleanup procedures
- Performance considerations

5. Test Implementation Details
For each test class/method:
- Purpose and scope of tests
- Test data setup and prerequisites
- Expected outcomes and assertions
- API documentation snippets
- Cleanup requirements
- Known limitations or constraints

6. API Testing Patterns
Document patterns for:
- Request/Response documentation
- Input validation testing
- Error response testing
- Authentication/Authorization testing
- Pagination testing
- File upload/download testing
- Async operation testing

7. Test Execution Flow
Include diagrams showing:
- Test setup and documentation generation flow
- Test data flow
- Mock interaction patterns
- Verification steps

Include Mermaid diagrams for:
1. Test hierarchy and organization
2. Test execution lifecycle
3. Documentation generation process
4. Mock interaction patterns

8. Documentation Generation
- REST Docs snippet configuration
- Custom snippet creation
- Documentation assembly process
- Template customization
- Output format configuration
- Version management

9. Best Practices
- Document naming conventions
- Describe assertion strategies
- Explain test isolation approaches
- Detail documentation maintenance
- Performance optimization techniques

10. Example Documentation
Include examples of:
- REST Docs test cases
- Generated documentation snippets
- Custom documentation templates
- Common test patterns
- Documentation customization

Remember to use clear, concise language and provide practical examples. Focus on both test maintainability and comprehensive API documentation. Response markdown documentation only. Use markdown format.
'''

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

3. Technical Considerations
- Error handling strategies
- Common patterns and conventions
- Performance considerations
- Testing approaches

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

#doc 번역
TRANSLATE_PROMPT = '''당신은 전문 번역가입니다. 제가 제공하는 마크다운 문서를 한국어로 번역해주세요.

번역 시 다음 지침을 반드시 따라주세요:

1. 마크다운 문법과 서식은 그대로 보존해주세요:
   - 제목 기호(#)
   - 글머리 기호(-, *, +)
   - 강조 표시(**bold**, *italic*)
   - 링크 형식([text](url))
   - 코드 블록(```)
   - 인용구(>)
   - 표 형식(|)

2. 번역 시 주의사항:
   - 전문 용어는 일반적으로 통용되는 한국어 용어를 사용해주세요
   - 코드 블록 내부의 코드와 주석을 구분하여, 코드는 그대로 두고 주석만 번역해주세요
   - URL, 이메일 주소, 변수명 등 고유 명사는 번역하지 마세요
   - 자연스러운 한국어 문장이 되도록 의역이 필요한 경우 의역을 해주세요
   - 기술 문서의 경우 한국의 기술 문서 작성 관행을 따라주세요

3. 원문의 의미와 뉘앙스를 정확하게 전달하면서도, 한국어 사용자가 이해하기 쉽게 번역해주세요.

아래 마크다운을 위 지침에 따라 한국어로 번역해주세요:

'''

PROMPT_README = f"""Please analyze the entire repository structure and generate a README.md in the following format:

# [Project Name]

## 🖼 Preview


##  Table of Contents

- [ Overview](#-overview)
- [ Analysis](#-features)
- [ Project Structure](#-project-structure)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)


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
-don't have expose all sections, Skip sections if no relevant technology is used.
-if you need to make sections, you can make sections like this:
- Frontend: [e.g., React, Vue, Angular]
- Backend: [e.g., Node.js, Python, Java]
- Database: [e.g., PostgreSQL, MongoDB]
- Other Sections(AI, Model, etc.): [e.g., Python, Java]

## 📊 Analysis
[Key analysis findings]
- Data analysis results
- Performance metrics
- Key insights
<!-- Summary of main points from Service.md -->

## 📁 Project Structure
-don't have expose all files, expose important files with Key Features
```
[project name]
├── 📁 [folder1]
│   ├── [file1]
│   └── [file2]
├── 📁 [folder2]
│   ├── [file1]
│   └── [file2]
└── ...
```

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies

### Installation
```bash
# Clone the repository
git clone [repository URL]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```
"""

PROMPT_USAGE = """Please analyze the entire build files, structure and generate in the following format:

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies
- Package manager
- Database system
- Version control system
- Others (AI, Model, etc.)

### Installation
```bash
# Clone the repository
git clone [repository URL]
cd [project-directory]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```
"""

DALLE_PROMPT = '''
Draw the core features clearly. 
A simple vector logo for project.
project : '''

CHATBOT_PROMPT = """You are a helpful assistant.

When answering:
1. Only use information from the provided context and chat history
2. If the context is relevant but insufficient to fully answer the query, use information from the chat history
3. If you're unsure about the relevance of the context, explain why
4. Never make up information that's not in the context

Remember to:
- Be concise and direct
- Cite specific parts of the context when relevant
- Maintain a helpful and professional tone"""

# CHATBOT_PROMPT = """You are an advanced technical assistant specialized in architectural problem-solving and error diagnosis. Your primary objective is to provide comprehensive, layer-by-layer analysis of technical issues.

# Core Problem-Solving Principles:
# 1. Architectural Layer Analysis
#    - Systematically investigate each architectural layer
#    - Trace error propagation across layers
#    - Identify potential root causes at each layer

# 2. Diagnostic Approach
#    - Provide detailed, context-specific guidance
#    - Explain not just the "what" but the "why"
#    - Offer actionable, implementable solutions

# 3. Comprehensive Error Investigation

# Diagnostic Framework:

# ### Layer-Specific Error Analysis
# #### Presentation Layer (Controller)
# - Analyze request mapping and validation
# - Examine method signatures and parameter handling
# - Check exception propagation mechanisms

# #### Service Layer
# - Review service method implementations
# - Validate business logic and transaction management
# - Inspect method-level error handling

# #### Repository Layer
# - Examine database query methods
# - Verify data access and retrieval strategies
# - Check query optimization and performance

# #### Domain Layer
# - Validate domain model constraints
# - Review business rules and entity relationships
# - Analyze state management and invariants

# ### Error Resolution Strategy
# 1. Contextual Error Tracing
#    - Map error symptoms to specific architectural layers
#    - Correlate error origins with system dependencies
#    - Prioritize investigation based on potential impact

# 2. Diagnostic Recommendations
#    - Provide code snippet examples for resolution
#    - Suggest refactoring approaches
#    - Highlight potential architectural improvements

# 3. Best Practices and Patterns
#    - Recommend architectural design patterns
#    - Suggest error handling and logging improvements
#    - Provide guidelines for robust system design

# ### Additional Investigative Techniques
# - Cross-layer dependency analysis
# - Performance and scalability considerations
# - Security and validation checks
# - Logging and monitoring recommendations

# Response Guidelines:
# - Be precise and technically detailed
# - Use clear, structured explanations
# - Provide concrete, implementable solutions
# - Focus on systemic improvements, not just quick fixes

# Output Format:
# 1. Error Context and Symptoms
# 2. Layer-by-Layer Diagnostic Analysis
# 3. Recommended Solutions
# 4. Potential Architectural Improvements
# 5. Code Refactoring Suggestions

# Always prioritize:
# - Systematic problem-solving
# - Architectural integrity
# - Long-term system maintainability
# """


PROMPT_README_GEMINI = f"""
analyze the code and generate only one README in the following format:

# [Project Name]

## 🖼 Preview


##  Table of Contents

- [ Overview](#-overview)
- [ Analysis](#-features)
- [ Project Structure](#-project-structure)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)


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
-don't have expose all sections, Skip sections if no relevant technology is used.
- Frontend: [e.g., React, Vue, Angular]
- Backend: [e.g., Node.js, Python, Java]
- Database: [e.g., PostgreSQL, MongoDB]
- Other Tools: [e.g., Docker, Redis]

## 📊 Analysis
[Key analysis findings]
- Data analysis results
- Performance metrics
- Key insights
<!-- Summary of main points from Service.md -->

## 📁 Project Structure
-don't have expose all files, expose important files with Key Features
```
[project name]
├── 📁 [folder1]
│   ├── [file1]
│   └── [file2]
├── 📁 [folder2]
│   ├── [file1]
│   └── [file2]
└── ...
```

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies

### Installation
```bash
# Clone the repository
git clone [repository URL]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```
"""

PROMPT_README_FROM_SUMMARY = f"""
Please create a README based on the provided README in the following format:

# [Project Name]

## 🖼 Preview


##  Table of Contents

- [ Overview](#-overview)
- [ Analysis](#-features)
- [ Project Structure](#-project-structure)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)


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
-don't have expose all sections, Skip sections if no relevant technology is used.
- Frontend: [e.g., React, Vue, Angular]
- Backend: [e.g., Node.js, Python, Java]
- Database: [e.g., PostgreSQL, MongoDB]
- Other Tools: [e.g., Docker, Redis]

## 📊 Analysis
[Key analysis findings]
- Data analysis results
- Performance metrics
- Key insights
<!-- Summary of main points from Service.md -->

## 📁 Project Structure
-don't have expose all files, expose important files with Key Features
```
[project name]
├── 📁 [folder1]
│   ├── [file1]
│   └── [file2]
├── 📁 [folder2]
│   ├── [file1]
│   └── [file2]
└── ...
```

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies

### Installation
```bash
# Clone the repository
git clone [repository URL]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```
"""

DALLE_PROMPT = '''
Draw the core features clearly. 
A simple vector logo for project.
project : '''

PROMPT_README_KOREAN = f"""Please analyze the entire repository structure and generate a README.md in the following format:

# [Project Name]

## 🖼 Preview


##  Table of Contents

- [ Overview](#-overview)
- [ Analysis](#-features)
- [ Project Structure](#-project-structure)
- [ Getting Started](#-getting-started)
  - [ Prerequisites](#prerequisites)
  - [ Installation](#installation)
  - [ Usage](#usage)


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
-don't have expose all sections, Skip sections if no relevant technology is used.
-if you need to make sections, you can make sections like this:
- Frontend: [e.g., React, Vue, Angular]
- Backend: [e.g., Node.js, Python, Java]
- Database: [e.g., PostgreSQL, MongoDB]
- Other Sections(AI, Model, etc.): [e.g., Python, Java]

## 📊 Analysis
[Key analysis findings]
- Data analysis results
- Performance metrics
- Key insights
<!-- Summary of main points from Service.md -->

## 📁 Project Structure
-don't have expose all files, expose important files with Key Features
```
[project name]
├── 📁 [folder1]
│   ├── [file1]
│   └── [file2]
├── 📁 [folder2]
│   ├── [file1]
│   └── [file2]
└── ...
```

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies

### Installation
```bash
# Clone the repository
git clone [repository URL]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```

MUST reponse all readme and annotations in Korean. except for the code and Project Name.
"""


PROMPT_USAGE_KOREAN = """Please analyze the entire build files, structure and generate in the following format:

## 🚀 Getting Started
-If there is not enough information, do not need to write it.
### Prerequisites
- Required environment setup
- Required dependencies
- Package manager
- Database system
- Version control system
- Others (AI, Model, etc.)

### Installation
```bash
# Clone the repository
git clone [repository URL]
cd [project-directory]

# Install required packages
[installation commands]

# Configure environment
[configuration commands]
```

### Usage
-If there is not enough information, do not need to write it.
```bash
# How to run
[execution commands]
```

MUST reponse in Korean. 
"""

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

3. Technical Considerations
- Error handling strategies
- Common patterns and conventions
- Performance considerations
- Testing approaches

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

SERVICE_DOC_PROMPT_KOREAN = '''다음 지침에 따라 제공된 Spring Service 코드에 대한 포괄적인 문서를 한국어로 작성하세요:

1. 서비스 개요
- 서비스의 목적과 책임에 대한 높은 수준의 개요로 시작
- 제공되는 주요 비즈니스 작업 문서화
- 서비스에서 노출된 모든 공개 메서드 나열
- 트랜잭션 요구 사항 문서화
- 일반적인 오류 시나리오 및 처리 접근 방식 문서화

2. 비즈니스 로직 처리
- 각 공개 메서드에 대해 다음 항목 문서화:
  * 메서드 시그니처 및 목적
  * 입력 매개변수 및 유효성 검사 규칙
  * 예상 반환 값
  * 트랜잭션 경계 및 격리 수준
  * 비즈니스 규칙 및 유효성 검사 논리
  * 오류 시나리오 및 처리 전략
  * 사용 코드 예제

3. 상세 구성 요소 문서화
각 구성 요소에 대해 다음을 제공:

a. 서비스 클래스:
- 클래스 이름 및 비즈니스 목적
- 의존성 주입 및 자동 와이어링된 구성 요소
- 트랜잭션 관리 구성
- 예외 처리 전략
- 유효성 검사 접근 방식

b. 비즈니스 DTO:
- 필드 설명 및 유효성 검사 제약 조건
- 데이터 변환/매핑 논리
- 도메인 모델 관계

4. 통합 지점
다음과의 상호작용 문서화:
- 리포지토리 및 데이터베이스 작업
- 다른 서비스
- 외부 시스템 (해당되는 경우)
- 이벤트 게시/처리 (해당되는 경우)

5. 구현 흐름
다음을 보여주는 다이어그램 포함:
- 비즈니스 로직 처리 파이프라인
- 서비스-리포지토리 상호작용
- 오류 처리 흐름
- 트랜잭션 경계

Mermaid 다이어그램 포함:
1. 서비스 종속성을 보여주는 구성 요소 다이어그램
2. 비즈니스 로직 흐름을 보여주는 시퀀스 다이어그램
3. 복잡한 작업에 대한 상태 다이어그램 (해당되는 경우)

6. 테스트 고려사항
- 주요 테스트 시나리오 문서화
- 모킹 요구 사항 설명
- 고려해야 할 중요한 비즈니스 엣지 케이스 나열

명확하고 간결한 언어를 사용하고 필요한 경우 컨텍스트를 제공하세요. 각 비즈니스 메서드에 대한 일반적인 사용 예제와 코드 조각을 포함하세요. 문서만 응답하세요. 마크다운 형식을 사용하세요.
'''

CONTROLLER_DOC_PROMPT_KOREAN = ''''Please provide comprehensive documentation for the given Spring Controller code, following these guidelines:

1. Controller Overview
- Begin with a high-level overview of the Controller's purpose and responsibilities
- Document the base URL path and any common request mappings
- List all REST endpoints exposed by the controller
- Describe authentication/authorization requirements
- Document common response formats and status codes

2. Request Handling
- Document each @RequestMapping method including:
  * HTTP method (GET, POST, etc.)
  * URL path and parameters
  * Request body format (if applicable)
  * Required headers or cookies
  * Expected response format
  * Possible response status codes and their meanings
  * Error handling and validation

3. Detailed Component Documentation
For each component, provide:

a. Controller Class:
- Class name and purpose
- Dependency injections and autowired components
- Cross-cutting concerns (logging, validation, etc.)
- Security annotations and access control
- Exception handling strategies

b. Request/Response DTOs:
- Field descriptions and validation constraints
- Data transformation/mapping logic
- Serialization/deserialization details

4. Integration Points
- Document interactions with:
  * Services and repositories
  * External APIs or systems
  * Message queues or events
  * Caching mechanisms

5. Implementation Flow
Include diagrams showing:
- Request processing pipeline
- Controller-Service-Repository interaction
- Error handling flow
- Authentication/Authorization flow

Include Mermaid diagrams for:
1. Component diagram showing controller dependencies
2. Sequence diagram showing request processing flow
3. State diagram for complex operations (if applicable)

6. Testing Considerations
- Document key test scenarios
- Describe mocking requirements
- List critical edge cases to consider

Remember to use clear, concise language and provide context where necessary. Include common usage examples and curl commands for API endpoints. Response documentation only. Use markdown format. Must response in Korean.
'''


CONTROLLER_DOC_PROMPT_KOREAN2 = '''
제공된 Controller 코드에 나와있는 모든 API에 대해 분석하고 다음 형식으로 한국어로 응답하세요:

# API 상세 분석 및 흐름 다이어그램 가이드

## API 이름

### API 엔드포인트 상세 분석
- **엔드포인트 URL**: 
- **HTTP 메서드**: 
- **요청 파라미터/본문**:
- **응답 구조**:

### 각 API 흐름 분석 템플릿

#### 1. 컨트롤러(Controller) 계층 분석
- **메서드 시그니처**:
- **HTTP 매핑 어노테이션**:
- **요청 데이터 처리**:
- **호출되는 서비스 메서드**:

#### 2. 서비스(Service) 계층 분석
- **비즈니스 로직 상세**:
- **데이터 변환 로직**:
- **호출되는 리포지토리 메서드**:

#### 3. 리포지토리(Repository) 계층 분석
- **수행되는 데이터베이스 작업**:
- **쿼리 메서드 상세**:
- **데이터 조회/변환 방식**:

#### 4. Mermaid 흐름 다이어그램
```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant Repository
    participant Database

    Client->>Controller: HTTP 요청
    Controller->>Service: 데이터 전달
    Service->>Repository: 데이터베이스 작업 요청
    Repository->>Database: 쿼리 실행
    Database-->>Repository: 결과 반환
    Repository-->>Service: 도메인 객체 반환
    Service-->>Controller: 비즈니스 로직 처리 결과
    Controller-->>Client: HTTP 응답

#### 5. 예외 시나리오

- **가능한 예외 유형**:
- **예외 처리 방식**:


분석 가이드라인
- 각 API 엔드포인트를 개별적으로 분석
- 계층별 상세 흐름과 로직 설명
- Mermaid 다이어그램을 통한 시각적 표현
- 한국어로 응답
'''

TEST_DOC_PROMPT_KOREAN = '''Please provide comprehensive documentation for the given Spring Test code, following these guidelines:

1. Test Suite Overview
- Describe the scope and purpose of the test suite
- Document test categories (unit, integration, e2e)
- List key testing frameworks and tools used (JUnit, REST Docs, etc.)
- Explain test configuration and setup

2. API Documentation Tests
- Document REST Docs test configuration
- Detail API documentation generation process
- For each API endpoint test:
  * HTTP request specifications
    - Method, path, parameters
    - Headers and authentication
    - Request body structure
    - Example request payloads
  * HTTP response specifications
    - Status codes and their meanings
    - Response headers
    - Response body structure
    - Example response payloads
  * Validation constraints
  * Error scenarios and responses

3. Test Environment
- Document required configuration properties
- Describe test database setup
- Detail mock services and test doubles
- Explain test data preparation
- Document required Spring profiles

4. Test Categories
For each test category, document:

a. Unit Tests:
- Test class structure and naming conventions
- Mocking strategies and tools
- Common test utilities and helpers
- Test lifecycle management

b. Integration Tests:
- Test container configuration
- Database initialization scripts
- External service mocks
- Security configuration for tests
- API contract validation tests

c. End-to-End Tests:
- Test environment setup
- Data seeding approach
- Cleanup procedures
- Performance considerations

5. Test Implementation Details
For each test class/method:
- Purpose and scope of tests
- Test data setup and prerequisites
- Expected outcomes and assertions
- API documentation snippets
- Cleanup requirements
- Known limitations or constraints

6. API Testing Patterns
Document patterns for:
- Request/Response documentation
- Input validation testing
- Error response testing
- Authentication/Authorization testing
- Pagination testing
- File upload/download testing
- Async operation testing

7. Test Execution Flow
Include diagrams showing:
- Test setup and documentation generation flow
- Test data flow
- Mock interaction patterns
- Verification steps

Include Mermaid diagrams for:
1. Test hierarchy and organization
2. Test execution lifecycle
3. Documentation generation process
4. Mock interaction patterns

8. Documentation Generation
- REST Docs snippet configuration
- Custom snippet creation
- Documentation assembly process
- Template customization
- Output format configuration
- Version management

9. Best Practices
- Document naming conventions
- Describe assertion strategies
- Explain test isolation approaches
- Detail documentation maintenance
- Performance optimization techniques

10. Example Documentation
Include examples of:
- REST Docs test cases
- Generated documentation snippets
- Custom documentation templates
- Common test patterns
- Documentation customization

Remember to use clear, concise language and provide practical examples. Focus on both test maintainability and comprehensive API documentation. Response markdown documentation only. Use markdown format. Must response in Korean.
'''

NEW_PROMPT_CONTROLLER_DOC = '''
다음 Spring Controller 파일을 분석하여 마크다운 형식의 API 문서를 생성해주세요:

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

#### 참고사항
- 인증 요구사항
- 권한 설정
- 기타 주의사항

문서 작성 시 주의사항:
1. 모든 API 엔드포인트에 대해 위 형식을 반복해서 작성하세요
2. 실제 요청/응답 예시를 포함하세요
3. 가능한 모든 응답 상태 코드를 문서화하세요
4. 인증이나 권한이 필요한 경우 반드시 명시하세요
'''

NEW_PROMPT_SERVICE_DOC = '''
# [Service 이름]

## 클래스 개요
- **클래스명**: `ServiceName`
- **패키지**: `package.path`
- **역할**: 주요 책임과 역할
- **의존성**:
  - 의존성 1
  - 의존성 2

## 메서드 명세

### `methodName()`
#### 기능
- 메서드 설명

#### 파라미터
| 이름 | 타입 | 설명 |
|------|------|------|
| param1 | String | 설명 |

#### 반환값
- 타입: `ReturnType`
- 설명: 반환값 설명

#### 비즈니스 로직
1. 단계 1
2. 단계 2
3. 단계 3

#### 예외 처리
| 예외 클래스 | 발생 조건 | 처리 방법 |
|------------|-----------|-----------|
| Exception1 | 조건 설명 | 처리 설명 |


문서 작성 시 주의사항:
1. 모든 public 메서드에 대해 상세히 문서화하세요
2. 중요한 private 메서드도 포함하세요
'''

NEW_PROMPT_TEST_DOC = '''
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