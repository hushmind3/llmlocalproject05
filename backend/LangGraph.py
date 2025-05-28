# LangGraph.py

# LangGraph 라이브러리에서 ReAct 에이전트를 생성하는 함수는 더 이상 사용하지 않습니다.
# from langgraph.prebuilt import create_react_agent 

# 파이썬의 타입 힌팅을 위한 모듈들을 임포트합니다.
from typing import List, Any, Optional, Tuple, Dict
# LangChain의 기본 채팅 모델 타입을 임포트합니다.
from langchain_core.language_models import BaseChatModel 
# LangChain의 Ollama 챗 모델 래퍼를 임포트합니다.
from langchain_ollama import ChatOllama 
# LangChain의 메시지 클래스(HumanMessage, AIMessage)를 임포트합니다.
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# FastAPI에서 HTTP 예외를 발생시키기 위해 임포트합니다.
from fastapi import HTTPException 

# 파일 시스템 작업을 위해 os 모듈을 임포트합니다.
import os 
import uuid 
from datetime import datetime 
import asyncio 
import re # 정규 표현식 사용을 위해 임포트 (도구 호출 파싱)

# --- RAG(검색 증강 생성) 구현을 위한 LangChain 컴포넌트 임포트 ---
from langchain_community.document_loaders import TextLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_chroma import Chroma 
from langchain_core.tools import Tool as LangChainTool 

# --- 외부 모듈에서 핵심 함수들을 임포트합니다. ---
from db import init_db, save_chat_session, load_chat_session, get_all_session_titles, delete_chat_session
from model import load_llm_and_embedding_instance 
from agent import file_tools # agent.py에서 파일 시스템 제어 도구들을 임포트합니다.

# --- 전역 변수: LLM 인스턴스 및 RAG/도구 컴포넌트 관리 (싱글톤 패턴) ---
_global_llm_instance: Optional[ChatOllama] = None 
_global_embedding_model: Optional[Any] = None 
_global_rag_tool: Optional[LangChainTool] = None 
_initialization_lock = asyncio.Lock() 

# RAG 데이터 저장소 경로 설정
DATA_DIR = "./data"
CHROMA_DB_DIR = "./chroma_db"

# --- LLM 로드 함수 ---
async def _load_llm_instance() -> Optional[ChatOllama]: 
    """
    Ollama 서버에서 LLM 인스턴스를 로드하는 비동기 함수입니다.
    """
    global _global_llm_instance 

    if _global_llm_instance:
        return _global_llm_instance
    
    async with _initialization_lock: 
        if _global_llm_instance:
            return _global_llm_instance
            
        print("[LangGraph DEBUG] Loading LLM instance...") 
        try:
            OLLAMA_LLM_MODEL_NAME = "aroxima/eeve-korean_instruct-10.8b-expo:latest" 
            OLLAMA_BASE_URL = "http://localhost:11434"
            OLLAMA_REQUEST_TIMEOUT = 120.0

            llm = ChatOllama(
                model=OLLAMA_LLM_MODEL_NAME,
                base_url=OLLAMA_BASE_URL,
                request_timeout=OLLAMA_REQUEST_TIMEOUT
            )
            _global_llm_instance = llm
            print("[LangGraph DEBUG] LLM instance loaded successfully.") 
            return llm
        except Exception as e:
            print(f"[LangGraph DEBUG] ERROR loading LLM instance: {type(e).__name__} - {e}") 
            import traceback; traceback.print_exc() 
            return None

# --- RAG 초기화 및 도구 생성 함수 ---
async def _initialize_rag_components() -> Optional[LangChainTool]: 
    """
    RAG에 필요한 구성 요소들을 초기화하고 검색 도구를 반환합니다.
    """
    global _global_embedding_model, _global_rag_tool 

    if _global_rag_tool: 
        return _global_rag_tool

    llm_instance, embed_model_instance = await load_llm_and_embedding_instance() 
    if not embed_model_instance:
        print("[LangGraph DEBUG] ERROR: Embedding model not loaded for RAG. RAG tool will not be created.") 
        return None
    _global_embedding_model = embed_model_instance 

    documents = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        with open(os.path.join(DATA_DIR, "policy.txt"), "w", encoding="utf-8") as f:
            f.write("회사 정책: 점심 12-1시, 퇴근 6시, 야근 시 식대 제공.")
        with open(os.path.join(DATA_DIR, "products.txt"), "w", encoding="utf-8") as f:
            f.write("제품: 스마트폰, 태블릿. 스마트폰은 AI 기능 탑재.")
        print(f"[LangGraph DEBUG] Created dummy {DATA_DIR} files.") 
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_DIR, filename)
            loader = TextLoader(file_path)
            documents.extend(loader.load())
    
    if not documents:
        print("[LangGraph DEBUG] No documents found in DATA_DIR for RAG. RAG tool will not be created.") 
        return None
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    if os.path.exists(CHROMA_DB_DIR) and len(os.listdir(CHROMA_DB_DIR)) > 0:
        print(f"[LangGraph DEBUG] Loading ChromaDB from {CHROMA_DB_DIR}...") 
        vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=_global_embedding_model)
    else:
        print(f"[LangGraph DEBUG] Creating new ChromaDB at {CHROMA_DB_DIR} and embedding documents...") 
        vectorstore = Chroma.from_documents(documents=splits, embedding=_global_embedding_model, persist_directory=CHROMA_DB_DIR)
        vectorstore.persist() 
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 

    rag_tool = LangChainTool(
        name="query_knowledge_base",
        description="""
        회사 정책, 제품 정보 등 로컬 지식 기반에서 답변을 찾아야 할 때 사용합니다.
        주어진 질문에 대해 가장 관련성이 높은 문서를 검색합니다.
        """,
        func=retriever.invoke, 
    )
    _global_rag_tool = rag_tool 
    print("[LangGraph DEBUG] RAG components initialized and tool created.") 
    return rag_tool

# --- 핵심 채팅 처리 함수 (LangGraph 기반 - '도구 사용' 수동 구현) ---
async def process_chat_request(user_message: str, current_session_id: Optional[str] = None) -> Tuple[str, str]:
    """
    사용자로부터 받은 채팅 메시지를 처리하고, LLM을 통해 응답을 생성하여 반환합니다.
    세션 ID를 기반으로 대화 기록을 관리하고 SQLite DB에 저장합니다.
    LLM이 '도구'를 사용하도록 직접 프롬프트를 구성하고 응답을 파싱하여 도구를 호출합니다.
    """
    # 1. DB 초기화 (SQLite)
    init_db() 

    # 2. LLM 및 RAG/파일 시스템 도구 로드/초기화
    llm = await _load_llm_instance() 
    rag_tool = await _initialize_rag_components() 
    
    # 사용 가능한 모든 도구를 리스트로 만듭니다. (RAG 도구 + 파일 시스템 도구)
    all_tools = []
    if rag_tool:
        all_tools.append(rag_tool)
    all_tools.extend(file_tools) # agent.py에서 임포트한 파일 도구들 추가

    if not llm:
        print("[LangGraph DEBUG] ERROR: LLM is None. Cannot process request.") 
        raise HTTPException(status_code=503, detail="오류: LLM 사용 불가 (초기화 실패).")

    # 3. 세션 ID 결정 및 대화 기록 로드
    session_id = current_session_id if current_session_id else str(uuid.uuid4())
    chat_history: List[Dict] = load_chat_session(session_id) or [] 

    # 4. LLM에 전달할 대화 기록 형식 준비 (LangChain 메시지 형식)
    lc_chat_history: List[BaseMessage] = []
    for msg in chat_history:
        if msg["sender"] == "user":
            lc_chat_history.append(HumanMessage(content=msg["text"]))
        else: 
            lc_chat_history.append(AIMessage(content=msg["text"]))
    
    # 현재 사용자 메시지를 LangChain 형식 기록에 추가
    lc_chat_history.append(HumanMessage(content=user_message))

    # 5. 현재 사용자 메시지를 DB 저장용 기록에 추가
    chat_history.append({"sender": "user", "text": user_message, "timestamp": datetime.now().isoformat()})

    print(f"[LangGraph DEBUG] Processing chat request for session_id: {session_id}, message: {user_message[:30]}...") 
    
    final_response_text = "응답 생성 실패."
    
    try:
        # --- LLM에게 도구 사용을 지시하는 프롬프트 구성 ---
        # LLM에게 어떤 도구들이 있고 어떻게 사용하는지 설명합니다.
        tools_description = "\n\n사용 가능한 도구:\n"
        for tool in all_tools:
            tools_description += f"- {tool.name}: {tool.description}\n"
        tools_description += "\n\n"
        tools_description += "응답은 다음 형식으로 주십시오:\n"
        tools_description += "Call: tool_name(param1='value1', param2='value2')\n"
        tools_description += "Thought: 도구 사용 후 다음 단계에 대한 생각\n"
        tools_description += "Final Answer: 최종 답변 (도구를 사용하지 않을 경우 바로 이 형식으로 응답)\n"
        tools_description += "최종 답변만 할 경우: 최종 답변 내용\n"
        
        # LLM에 전달할 최종 프롬프트 (메시지 기록 + 도구 설명 + 현재 질문)
        # 현재 사용자 메시지를 포함하는 마지막 HumanMessage의 content를 업데이트하여 도구 설명을 포함시킵니다.
        # 기존 메시지 리스트에 영향을 주지 않도록 새로운 메시지 객체를 만듭니다.
        prompt_with_tools = list(lc_chat_history) # 리스트 복사
        
        # LLM이 도구 사용을 추론할 수 있도록 도구 설명을 프롬프트에 추가
        # (마지막 사용자 메시지에 도구 설명을 추가)
        prompt_with_tools[-1] = HumanMessage(content=user_message + tools_description)

        print(f"[LangGraph DEBUG] Invoking LLM with tools description and {len(prompt_with_tools)} messages...") 
        
        # 6. LLM 호출 및 응답 파싱
        # LLM에게 도구 설명을 포함한 프롬프트를 전달합니다.
        raw_llm_response_obj = await llm.ainvoke(prompt_with_tools)
        raw_llm_response_content = str(raw_llm_response_obj.content)
        print(f"[LangGraph DEBUG] Raw LLM response: {raw_llm_response_content[:100]}...") 

        # --- LLM 응답 파싱 및 도구 실행 ---
        # LLM 응답에서 'Call:' 패턴을 찾아 도구 호출을 파싱합니다.
        tool_call_match = re.search(r"Call:\s*(\w+)\((.*)\)", raw_llm_response_content, re.DOTALL)
        
        if tool_call_match:
            tool_name = tool_call_match.group(1)
            tool_args_str = tool_call_match.group(2)
            
            # 파싱된 인자 문자열을 파이썬 딕셔너리로 변환
            try:
                # 안전한 eval 대신 json.loads와 같은 방식을 사용하기 위해 더미 JSON 형태로 변환
                # (eval은 보안 위험이 있으므로 실제 프로덕션에서는 사용하지 않는 것이 좋습니다.)
                # 여기서는 테스트를 위해 eval을 사용합니다.
                tool_args = eval(f"dict({tool_args_str})") # "param='value'" -> {'param':'value'}
            except Exception as e:
                print(f"[LangGraph DEBUG] ERROR parsing tool arguments: {e}. Raw args: {tool_args_str}") # DEBUG
                tool_args = {} # 파싱 실패 시 빈 인자로 처리

            print(f"[LangGraph DEBUG] LLM requested tool call: {tool_name} with args: {tool_args}") # DEBUG
            
            tool_output = "도구 실행 실패 또는 찾을 수 없음."
            found_tool_func = None
            for tool_item in all_tools:
                if tool_item.name == tool_name:
                    found_tool_func = tool_item.func
                    break
            
            if found_tool_func:
                try:
                    # 도구 함수 호출
                    tool_output = await asyncio.to_thread(found_tool_func, **tool_args)
                    print(f"[LangGraph DEBUG] Tool '{tool_name}' executed. Output: {tool_output[:50]}...") # DEBUG
                    
                    # 도구 실행 결과를 다시 LLM에게 전달하여 최종 답변을 생성하도록 합니다.
                    # 이 과정은 LangGraph의 일반적인 에이전트 루프에서 자동으로 처리되지만,
                    # 여기서는 수동으로 한번 더 LLM을 호출합니다.
                    lc_chat_history.append(AIMessage(content=raw_llm_response_content)) # LLM의 도구 호출 지시
                    lc_chat_history.append(HumanMessage(content=f"Tool Output: {tool_output}")) # 도구 실행 결과
                    
                    print("[LangGraph DEBUG] Invoking LLM again with tool output...") # DEBUG
                    final_response_obj = await llm.ainvoke(lc_chat_history)
                    final_response_text = str(final_response_obj.content)

                except Exception as tool_e:
                    tool_output = f"도구 실행 중 오류 발생: {type(tool_e).__name__} - {tool_e}"
                    print(f"[LangGraph DEBUG] Tool execution ERROR: {tool_output}") # DEBUG
                    final_response_text = f"죄송합니다. 도구 실행 중 오류가 발생했습니다: {tool_output}"
            else:
                final_response_text = f"죄송합니다. 요청하신 도구 '{tool_name}'을(를) 찾을 수 없습니다."

        else:
            # LLM이 도구 호출 형식에 맞게 응답하지 않았다면, 일반적인 답변으로 간주합니다.
            print("[LangGraph DEBUG] LLM did not request a tool. Responding directly.") # DEBUG
            final_response_text = raw_llm_response_content # LLM의 원본 응답을 최종 답변으로 사용

        print(f"[LangGraph DEBUG] Final processed response: {final_response_text[:50]}...") 
        
        # 7. AI 응답을 DB 저장용 기록에 추가
        chat_history.append({"sender": "ai", "text": final_response_text, "timestamp": datetime.now().isoformat()})
        
        # 8. 현재 세션의 대화 기록을 SQLite DB에 저장/업데이트
        session_title = user_message[:30] + "..." if len(user_message) > 30 else user_message
        save_chat_session(session_id, session_title, chat_history)
        print(f"[LangGraph DEBUG] Session '{session_id}' chat history saved.") 

        return final_response_text, session_id 

    except Exception as e: 
        print(f"[LangGraph DEBUG] ERROR during agent invocation or response processing: {type(e).__name__} - {e}") 
        import traceback; traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"LLM 처리 중 오류: {type(e).__name__}")
