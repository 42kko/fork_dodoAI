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