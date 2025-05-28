# db.py

# import (키워드): 다른 파이썬 파일이나 라이브러리(모듈)에 있는 기능을 현재 파일로 가져올 때 사용합니다.
# sqlite3 (모듈): 파이썬에 기본 내장된 SQLite 데이터베이스와의 인터페이스를 제공하는 모듈입니다.
#                 별도의 서버 없이 파일 형태로 데이터베이스를 관리할 수 있게 해줍니다.
import sqlite3
# json (모듈): JSON(JavaScript Object Notation) 데이터를 파이썬 객체로, 파이썬 객체를 JSON 문자열로 변환하는 기능을 제공합니다.
#             채팅 메시지 목록(리스트)을 SQLite DB의 TEXT 컬럼에 저장하고 불러올 때 사용됩니다.
import json
# uuid (모듈): 고유한 식별자(Universally Unique Identifier)를 생성하기 위해 사용됩니다.
#             채팅 세션의 고유 ID를 만들 때 사용됩니다.
import uuid
# datetime (모듈): 날짜와 시간을 다루기 위해 사용됩니다.
#                 채팅 메시지의 타임스탬프나 세션의 마지막 업데이트 시간을 저장할 때 사용됩니다.
from datetime import datetime
# typing (모듈): 파이썬에서 변수나 함수의 입/출력 데이터 '타입'을 명시하는 기능을 제공하는 모듈입니다.
# List (타입): '이 변수는 여러 항목을 담는 목록(리스트)이야'라고 알려줍니다.
# Dict (타입): '이 변수는 키(key)와 값(value)으로 이루어진 사전(딕셔너리)이야'라고 알려줍니다.
# Optional (타입): '이 변수는 지정된 타입이거나 None(값이 없음)일 수 있어'라고 알려줍니다.
# Tuple (타입): '이 변수는 여러 항목을 순서대로 담는 튜플이야'라고 알려줍니다.
from typing import List, Dict, Optional, Tuple

# --- SQLite DB 파일 경로 정의 ---
# DB_FILE (변수 - 사용자 정의): SQLite 데이터베이스 파일의 경로와 이름을 정의하는 변수입니다.
#                            이 파일은 백엔드 프로젝트 루트(예: project05\backend) 아래에 생성됩니다.
DB_FILE = "./chat_history.db"

# def (키워드): 새로운 '함수(Function)'를 정의할 때 사용하는 키워드입니다.
# init_db (함수 - 사용자 정의): 데이터베이스를 초기화하고 테이블을 생성하는 함수입니다.
def init_db():
    """
    SQLite 데이터베이스를 초기화하고, 필요한 테이블을 생성합니다.
    이 함수는 애플리케이션 시작 시 (또는 첫 DB 작업 시) 한 번만 호출되어야 합니다.
    """
    # sqlite3.connect (함수 - sqlite3 모듈): 지정된 DB_FILE (변수)에 연결합니다.
    #                                    파일이 없으면 자동으로 새 파일을 생성합니다.
    conn = sqlite3.connect(DB_FILE)
    # .cursor (메서드): 데이터베이스 명령(SQL 쿼리)을 실행하는 데 사용되는 커서 객체를 생성합니다.
    cursor = conn.cursor()
    # .execute (메서드): SQL 쿼리 문자열을 실행합니다.
    # CREATE TABLE IF NOT EXISTS (SQL 구문): 'chat_sessions' 테이블이 없으면 생성합니다.
    # PRIMARY KEY (SQL 구문): 'session_id'를 테이블의 기본 키로 설정합니다. (각 행을 고유하게 식별)
    # TEXT (SQL 데이터 타입): 문자열 데이터를 저장하는 컬럼 타입입니다.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT,
            messages TEXT,
            timestamp TEXT
        )
    """)
    # .commit (메서드): 현재까지의 모든 변경 사항(예: 테이블 생성)을 데이터베이스에 영구적으로 저장합니다.
    conn.commit()
    # .close (메서드): 데이터베이스 연결을 닫습니다.
    conn.close()
    # print (함수 - 파이썬 내장): 디버깅 메시지를 콘솔에 출력합니다.
    print(f"[DB DEBUG] SQLite DB initialized and table created at {DB_FILE}")

# def (키워드): 새로운 함수를 정의합니다.
# save_chat_session (함수 - 사용자 정의): 채팅 세션 데이터를 저장하거나 업데이트하는 함수입니다.
# session_id (매개변수): 저장할 세션의 고유 ID (문자열).
# title (매개변수): 세션의 제목 (문자열).
# messages (매개변수): 세션의 모든 채팅 메시지 목록 (딕셔너리 리스트).
def save_chat_session(session_id: str, title: str, messages: List[Dict]) -> None:
    """
    특정 채팅 세션의 메시지 목록을 SQLite DB에 저장하거나 업데이트합니다.
    messages는 Dict 리스트여야 하며, JSON 문자열로 변환하여 저장합니다.
    """
    conn = sqlite3.connect(DB_FILE) # sqlite3.connect (함수)
    cursor = conn.cursor() # .cursor (메서드)
    # json.dumps (함수 - json 모듈): 파이썬 리스트(messages)를 JSON 형식의 문자열로 변환합니다.
    #                               DB의 TEXT 컬럼에 저장하기 위함입니다.
    messages_json = json.dumps(messages)
    # datetime.now() (함수 - datetime 모듈): 현재 날짜와 시간을 가져옵니다.
    # .isoformat() (메서드): 날짜와 시간을 ISO 8601 형식의 문자열로 변환합니다.
    current_time = datetime.now().isoformat() 

    # .execute (메서드): SQL 쿼리를 실행합니다.
    # INSERT OR REPLACE INTO (SQL 구문): 'session_id'가 이미 존재하면 해당 행을 업데이트하고, 없으면 새로 삽입합니다.
    # VALUES (?, ?, ?, ?) (SQL 구문): 물음표(?)는 나중에 실제 값이 들어갈 '플레이스홀더'입니다.
    cursor.execute("""
        INSERT OR REPLACE INTO chat_sessions (session_id, title, messages, timestamp)
        VALUES (?, ?, ?, ?)
    """, (session_id, title, messages_json, current_time)) # 플레이스홀더에 실제 값들을 튜플로 전달합니다.
    conn.commit() # .commit (메서드): 변경 사항을 DB에 저장합니다.
    conn.close() # .close (메서드)
    # print (함수 - 파이썬 내장)
    # print(f"[DB DEBUG] Chat session '{session_id}' saved/updated.") # DEBUG 제거

def load_chat_session(session_id: str) -> Optional[List[Dict]]: # load_chat_session (함수 - 사용자 정의)
    """
    특정 채팅 세션 ID에 해당하는 메시지 목록을 SQLite DB에서 불러옵니다.
    """
    conn = sqlite3.connect(DB_FILE) # sqlite3.connect (함수)
    cursor = conn.cursor() # .cursor (메서드)
    # .execute (메서드): SELECT (SQL 구문) 쿼리를 실행하여 'messages' 컬럼의 값을 가져옵니다.
    # WHERE (SQL 구문): 특정 조건(session_id가 일치하는)에 해당하는 행만 선택합니다.
    cursor.execute("SELECT messages FROM chat_sessions WHERE session_id = ?", (session_id,))
    # .fetchone (메서드): 쿼리 결과 중 첫 번째 행을 튜플 형태로 가져옵니다. 결과가 없으면 None을 반환합니다.
    row = cursor.fetchone()
    conn.close() # .close (메서드)
    # if (조건문): row (변수)에 값이 있다면 (세션을 찾았다면)
    if row:
        # json.loads (함수 - json 모듈): DB에서 읽어온 JSON 문자열(row[0])을 파이썬 리스트로 다시 변환합니다.
        return json.loads(row[0]) 
    # print (함수 - 파이썬 내장)
    # print(f"[DB DEBUG] Chat session '{session_id}' not found.") # DEBUG 제거
    # None (값): 세션을 찾지 못하면 None을 반환합니다.
    return None

def get_all_session_titles() -> List[Dict[str, str]]: # get_all_session_titles (함수 - 사용자 정의)
    """
    저장된 모든 채팅 세션의 ID와 제목, 마지막 업데이트 시간 목록을 반환합니다.
    """
    conn = sqlite3.connect(DB_FILE) # sqlite3.connect (함수)
    cursor = conn.cursor() # .cursor (메서드)
    # .execute (메서드): 모든 세션의 ID, 제목, 타임스탬프를 가져옵니다.
    # ORDER BY (SQL 구문): 'timestamp' 컬럼을 기준으로 내림차순(DESC) 정렬하여 최신 세션이 먼저 오도록 합니다.
    cursor.execute("SELECT session_id, title, timestamp FROM chat_sessions ORDER BY timestamp DESC")
    # .fetchall (메서드): 쿼리 결과의 모든 행을 튜플들의 리스트 형태로 가져옵니다.
    rows = cursor.fetchall()
    conn.close() # .close (메서드)
    
    # sessions (변수 - 사용자 정의): 결과를 딕셔너리 리스트 형태로 변환하여 저장할 리스트입니다.
    sessions = []
    # for (키워드): rows (변수)의 각 행을 반복합니다.
    for row in rows:
        # .append (메서드): 리스트에 항목을 추가합니다.
        sessions.append({
            "session_id": row[0], # 튜플의 첫 번째 요소 (session_id)
            "title": row[1],      # 튜플의 두 번째 요소 (title)
            "timestamp": row[2]   # 튜플의 세 번째 요소 (timestamp)
        })
    # print (함수 - 파이썬 내장)
    # print(f"[DB DEBUG] Retrieved {len(sessions)} session titles.") # DEBUG 제거
    return sessions # 변환된 세션 목록 리스트 반환

def delete_chat_session(session_id: str) -> bool: # delete_chat_session (함수 - 사용자 정의)
    """
    특정 채팅 세션 ID에 해당하는 대화 기록을 DB에서 삭제합니다.
    성공 시 True, 실패 시 False를 반환합니다.
    """
    conn = sqlite3.connect(DB_FILE) # sqlite3.connect (함수)
    cursor = conn.cursor() # .cursor (메서드)
    # .execute (메서드): DELETE (SQL 구문) 쿼리를 실행하여 특정 조건(session_id가 일치하는)의 행을 삭제합니다.
    cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    conn.commit() # .commit (메서드): 변경 사항을 DB에 저장합니다.
    # .rowcount (속성): 마지막으로 실행된 쿼리에 의해 영향을 받은 행의 수를 반환합니다.
    deleted_rows = cursor.rowcount
    conn.close() # .close (메서드)
    # if (조건문): deleted_rows (변수)가 0보다 크다면 (삭제된 행이 있다면)
    if deleted_rows > 0:
        # print (함수 - 파이썬 내장)
        # print(f"[DB DEBUG] Chat session '{session_id}' deleted.") # DEBUG 제거
        return True # 삭제 성공 시 True 반환
    # print (함수 - 파이썬 내장)
    # print(f"[DB DEBUG] Chat session '{session_id}' not found for deletion.") # DEBUG 제거
    return False # 삭제 실패 시 False 반환
