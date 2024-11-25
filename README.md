# Moheng

## 🖼 Preview
![Preview Image](https://via.placeholder.com/800x400?text=Project+Preview)

##  Table of Contents

- [Moheng](#moheng)
  - [🖼 Preview](#-preview)
  - [Table of Contents](#table-of-contents)
  - [📝 Overview](#-overview)
    - [Main Purpose](#main-purpose)
    - [Key Features](#key-features)
    - [Core Technology Stack](#core-technology-stack)
  - [📊 Analysis](#-analysis)
  - [📁 Project Structure](#-project-structure)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)

## 📝 Overview
Moheng is a comprehensive travel planning application that integrates various features such as trip scheduling, user authentication, and personalized recommendations based on user preferences and historical data.

### Main Purpose
- The primary goal of Moheng is to provide users with a seamless travel planning experience by allowing them to create, manage, and share their travel itineraries.
- It solves the problem of disorganized travel plans by offering a structured platform for users to plan their trips effectively.
- The target audience includes travelers, travel enthusiasts, and anyone looking to organize their travel experiences.

### Key Features
- User authentication and profile management.
- Trip scheduling and itinerary management.
- Integration with external AI models for personalized trip recommendations.
- Live information and keyword-based trip suggestions.

### Core Technology Stack
- Frontend: React, Vite
- Backend: Spring Boot
- Database: PostgreSQL
- Other Sections: Python, FastAPI for AI model serving

## 📊 Analysis
The application utilizes various data analysis techniques to provide personalized recommendations based on user preferences and historical data. Key insights include:
- User engagement metrics and preferences are analyzed to improve recommendation algorithms.
- Performance metrics are monitored to ensure a responsive user experience.

## 📁 Project Structure
```
moheng
├── 📁 ai
│   ├── 📁 model_serving
│   │   ├── 📁 application
│   │   ├── 📁 domain
│   │   ├── 📁 infra
│   │   └── 📁 interface
│   └── ...
├── 📁 kakao-25
│   ├── 📁 moheng
│   │   ├── 📁 auth
│   │   ├── 📁 planner
│   │   ├── 📁 trip
│   │   └── ...
│   └── ...
└── ...
```

## 🚀 Getting Started

### Prerequisites
- **Required environment setup**: Docker, Java (JDK 22), Python (3.11)
- **Required dependencies**: 
  - For Backend: Spring Boot, JPA, H2 Database, MySQL Connector, JWT
  - For AI: FastAPI, Uvicorn, Poetry
  - For Frontend: React, Vite, Axios
- **Package manager**: 
  - For Python: Poetry
  - For Java: Gradle
  - For JavaScript: npm
- **Database system**: H2, MySQL
- **Version control system**: Git
- **Others**: Docker for containerization, Jenkins for CI/CD

### Installation
```bash
# Clone the repository
git clone https://github.com/kakao-25/moheng.git
cd moheng-develop

# Install required packages for Backend
cd backend
./gradlew build

# Install required packages for AI
cd ../ai
pip install poetry
poetry install

# Install required packages for Frontend
cd ../frontend
npm install
```

### Usage
```bash
# Run the Backend
cd backend
./gradlew bootRun

# Run the AI service
cd ../ai
poetry run python main.py

# Run the Frontend
cd ../frontend
npm start
```