# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager
import traceback
from typing import Optional, List, Any, Tuple, Dict

# LangGraph 모듈에서 핵심 함수들을 임포트합니다.
from LangGraph import process_chat_request, get_all_session_titles, load_chat_session, save_chat_session, delete_chat_session

# --- FastAPI 애플리케이션 정의 시작 ---
# Lifespan 이벤트 핸들러
@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB 초기화는 LangGraph.py 내부에서 _load_llm_instance 호출 시 (첫 요청 시) 일어납니다.
    yield
    # 애플리케이션 종료 시 실행될 코드 (예: DB 연결 종료 등)

# FastAPI 애플리케이션 인스턴스를 생성합니다.
app = FastAPI(lifespan=lifespan)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "FastAPI Backend is running."}

# Pydantic 모델
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None # 세션 ID 추가

# 채팅 엔드포인트
@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage):
    user_message = chat_message.message
    current_session_id = chat_message.session_id # 프론트엔드에서 받은 세션 ID

    try:
        # 핵심 채팅 처리 함수 호출 (세션 ID 전달)
        final_response_text, new_session_id = await process_chat_request(user_message, current_session_id)
        return {"response": final_response_text, "session_id": new_session_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"ERROR: Unhandled exception in /api/chat endpoint: {type(e).__name__} - {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"채팅 처리 중 예상치 못한 오류 발생: {type(e).__name__}.")

# 세션 목록 가져오기 엔드포인트
@app.get("/api/chat/sessions")
async def get_sessions_endpoint():
    try:
        sessions = get_all_session_titles()
        return {"sessions": sessions}
    except Exception as e:
        print(f"ERROR: Unhandled exception in /api/chat/sessions: {type(e).__name__} - {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"세션 목록 로드 중 오류: {type(e).__name__}.")

# 특정 세션 로드 엔드포인트 추가 (GET 메서드)
@app.get("/api/chat/session/{session_id}")
async def get_specific_session_endpoint(session_id: str):
    try:
        messages = load_chat_session(session_id)
        if messages is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
        return {"messages": messages} # 프론트엔드에서 기대하는 형식으로 반환
    except Exception as e:
        print(f"ERROR: Unhandled exception in /api/chat/session/{session_id} (GET): {type(e).__name__} - {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"세션 로드 중 오류: {type(e).__name__}.")

# 세션 삭제 엔드포인트
@app.delete("/api/chat/session/{session_id}")
async def delete_session_endpoint(session_id: str):
    try:
        success = delete_chat_session(session_id)
        if success:
            return {"message": f"Session {session_id} deleted successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found.")
    except Exception as e:
        print(f"ERROR: Unhandled exception in /api/chat/session/{session_id} (DELETE): {type(e).__name__} - {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"세션 삭제 중 오류: {type(e).__name__}.")

# --- FastAPI 애플리케이션 정의 종료 ---
