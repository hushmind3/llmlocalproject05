



# 🤖 AI-Powered RAG Chatbot (AI-Assisted Non-Developer Built, Local & Full-Stack) + Agent & MCP Features Under Development (Not Yet Implemented)
# 🤖 AI 기반 RAG 챗봇 (AI 활용 비개발자 제작, 로컬 구동 & 풀스택) + 에이전트 & MCP 기능 개발 중

This project implements a comprehensive AI chatbot solution with **Retrieval Augmented Generation (RAG)** capabilities, designed to run entirely in a local environment. Built from the ground up by a non-developer leveraging the power of AI tools, this system integrates a robust Python backend with a user-friendly React/Vite frontend to provide accurate and context-aware responses.

이 프로젝트는 **검색 증강 생성(RAG)** 기능을 갖춘 포괄적인 AI 챗봇 솔루션을 구현합니다. 전체를 로컬 환경에서 구동하도록 설계되었습니다. 코딩 경험이 없는 비개발자가 AI 도구를 활용하여 처음부터 구축했으며, 강력한 파이썬 백엔드와 사용자 친화적인 리액트/바이트 프론트엔드를 통합하여 정확하고 문맥을 인지하는 답변을 제공합니다.

## ✨ Key Features / 주요 기능

* **Local LLM Integration / 로컬 LLM 통합:** Designed for local AI model inference, ensuring data privacy and reducing reliance on cloud services. (데이터 프라이버시를 보장하고 클라우드 서비스에 대한 의존도를 줄이기 위해 로컬 AI 모델 추론에 최적화되었습니다.)
* **Retrieval Augmented Generation (RAG) / 검색 증강 생성 (RAG):** Enhances chatbot accuracy by retrieving relevant information from a custom knowledge base (ChromaDB) before generating responses. (맞춤형 지식 데이터베이스(ChromaDB)에서 관련 정보를 검색하여 답변을 생성함으로써 챗봇의 정확도를 향상시킵니다.)
* **Full-Stack Architecture / 풀스택 아키텍처:** Composed of a Python backend (FastAPI) and a React/Vite frontend for a complete, interactive experience. (파이썬 백엔드(FastAPI)와 리액트/바이트 프론트엔드로 구성된 풀스택 아키텍처로 완전하고 상호작용적인 사용자 경험을 제공합니다.)
* **Custom Knowledge Base / 맞춤형 지식 데이터베이스:** Utilizes ChromaDB and SQLite for managing and querying internal knowledge documents. (내부 지식 문서를 관리하고 쿼리하는 데 ChromaDB와 SQLite를 활용합니다.)
* **Modular Design / 모듈식 설계:** Built with LangChain and LangGraph for flexible and extensible AI workflows. (유연하고 확장 가능한 AI 워크플로우를 위해 LangChain 및 LangGraph로 구축되었습니다.)
* **Non-Developer Empowered Development / 비개발자의 AI 기반 개발:** AI 도구(Gemini, ChatGPT 등)가 기존 코딩 지식 없이도 복잡한 애플리케이션을 구축할 수 있도록 개인에게 어떻게 힘을 실어줄 수 있는지 보여주는 증거입니다.

## 🚀 Technologies Used / 사용 기술

### Backend / 백엔드
* **Python 3.13**
* **FastAPI:** High-performance web framework for building robust APIs. (강력한 API 구축을 위한 고성능 웹 프레임워크)
* **LangChain:** Framework for developing applications powered by language models. (언어 모델 기반 애플리케이션 개발 프레임워크)
* **LangGraph:** Building stateful, multi-actor applications with LLMs. (LLM으로 상태 저장형, 다중 액터 애플리케이션 구축)
* **ChromaDB:** Open-source embedding database for RAG. (RAG를 위한 오픈소스 임베딩 데이터베이스)
* **SQLite:** Lightweight database for managing chat history and basic data. (채팅 기록 및 기본 데이터 관리를 위한 경량 데이터베이스)
* **(Optional: Ollama/OpenAI API if used for specific model calls / 선택 사항: 특정 모델 호출에 Ollama/OpenAI API 사용 시)**

### Frontend / 프론트엔드
* **React:** A JavaScript library for building user interfaces. (사용자 인터페이스 구축을 위한 자바스크립트 라이브러리)
* **Vite:** Fast build tool for modern web projects. (현대 웹 프로젝트를 위한 빠른 빌드 도구)
* **(Optional: Next.js if used in conjunction with React/Vite / 선택 사항: React/Vite와 함께 Next.js 사용 시)**

## ⚙️ How to Run Locally / 로컬에서 실행하는 방법

To get this project up and running on your local machine, follow these steps:
(이 프로젝트를 로컬에서 실행하려면 다음 단계를 따르세요:)

### 1. Clone the Repository / 1. 저장소 복제

First, open your terminal/command prompt and navigate to the directory where you want to save the project. Then, clone this repository:
(먼저 터미널/명령 프롬프트를 열고 프로젝트를 저장할 디렉토리로 이동한 다음, 이 저장소를 복제합니다:)

```bash
git clone [https://github.com/hushmind3/llmlocalproject05.git](https://github.com/hushmind3/llmlocalproject05.git)
cd llmlocalproject05 # If your project folder is different, adjust accordingly (e.g., cd project05/git)

Note: If your project's root directory is project05/git on your local machine, after cloning, you might need to cd into that specific subdirectory: cd llmlocalproject05/git.
참고: 로컬 머신에서 프로젝트의 루트 디렉토리가 project05/git인 경우, 복제 후 해당 하위 디렉토리로 cd 해야 할 수 있습니다: cd llmlocalproject05/git.
2. Backend Setup & Run / 2. 백엔드 설정 및 실행
Navigate into the backend directory, set up the Python virtual environment, install dependencies, and run the server.
(백엔드 디렉토리로 이동하여 파이썬 가상 환경을 설정하고, 의존성을 설치한 후 서버를 실행합니다.)

cd backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server (using uvicorn as an example)
uvicorn main:app --reload # Adjust 'main:app' if your entry file is different

Note: You might need to set up environment variables (e.g., API keys if using external services) in a .env file within the backend directory. Refer to your backend code for required variables.
참고: 환경 변수(예: 외부 서비스를 사용하는 경우 API 키)를 backend 디렉토리 내의 .env 파일에 설정해야 할 수 있습니다. 필요한 변수는 백엔드 코드를 참조하세요.
3. Frontend Setup & Run / 3. 프론트엔드 설정 및 실행
Open a NEW terminal/command prompt window. Navigate into the frontend directory, install Node.js dependencies, and run the development server.
(새 터미널/명령 프롬프트 창을 엽니다. frontend 디렉토리로 이동하여 Node.js 의존성을 설치하고 개발 서버를 실행합니다.)

cd frontend

# Install Node.js dependencies (assuming npm is used)
npm install # or yarn install if you use yarn (if package.json exists)
# If no package.json, ensure all necessary JS files are linked/served correctly based on your project setup.
# (package.json 파일이 없다면, 프로젝트 설정에 따라 필요한 JS 파일들이 올바르게 연결/제공되는지 확인하세요.)

# Run the frontend development server
npm run dev # or yarn dev

4. Access the Chatbot / 4. 챗봇 접속
Once both the backend and frontend servers are running, open your web browser and navigate to the address where your frontend is serving (usually http://localhost:5173 for Vite, or similar).
(백엔드 및 프론트엔드 서버가 모두 실행되면 웹 브라우저를 열고 프론트엔드가 서비스되는 주소(일반적으로 Vite의 경우 http://localhost:5173 또는 유사한 주소)로 이동하세요.)

💡 Project Vision & Current Status / 프로젝트 비전 및 현재 상태
This project aims to demonstrate the potential of local LLMs for personalized and private AI applications.
(이 프로젝트는 개인화되고 프라이빗한 AI 애플리케이션을 위한 로컬 LLM의 잠재력을 보여주는 것을 목표로 합니다.)

Current Status / 현재 상태:
The implementation involved attempting to integrate agentic workflows using LangGraph. This part of the development is currently paused as I am in the process of finding solutions for specific challenges encountered during the agentic implementation. I am actively seeking solutions and learning more about advanced LangGraph patterns to complete this feature.

(LangGraph를 사용하여 에이전트 워크플로우를 통합하려는 구현을 진행했습니다. 이 개발 부분은 현재 에이전트 구현 중 직면한 특정 문제에 대한 해결책을 찾는 과정에 있어 중단된 상태입니다. 이 기능을 완성하기 위해 적극적으로 해결책을 찾고 더 고급 LangGraph 패턴을 학습하고 있습니다.)

🙏 Acknowledgements / 감사 말씀
Built with the invaluable assistance of AI (e.g., Gemini, ChatGPT) for guidance, debugging, and code generation. (가이드, 디버깅, 코드 생성 등 AI(예: Gemini, ChatGPT)의 귀중한 도움으로 구축되었습니다.)
Inspired by the open-source LLM community (LangChain, LangGraph, ChromaDB, Hugging Face). (오픈소스 LLM 커뮤니티(LangChain, LangGraph, ChromaDB, Hugging Face)에서 영감을 받았습니다.)
📜 License / 라이선스
This project is open-source and available under the MIT License (recommended, if you wish to apply one).
(이 프로젝트는 오픈소스이며 MIT 라이선스로 제공됩니다 (원하는 경우 적용 권장).)
