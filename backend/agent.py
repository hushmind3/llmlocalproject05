# agent.py

# import (키워드): 다른 파이썬 파일이나 라이브러리(모듈)에 있는 기능을 현재 파일로 가져올 때 사용합니다.
# os (모듈): 운영체제(Operating System)와 상호작용하는 파이썬의 기본 모듈입니다.
#            파일 생성, 읽기, 삭제, 디렉토리 목록 조회 등 실제 파일 시스템 작업을 수행하는 데 사용됩니다.
import os
# from (키워드): 특정 모듈(라이브러리) 안에서 특정 부분(클래스, 함수 등)만 선택적으로 가져올 때 사용합니다.
# langchain_core.tools (모듈): LangChain 라이브러리에서 도구 관련 기능을 제공하는 모듈입니다.
# Tool (클래스): LangChain 라이브러리에서 제공하는 '도구'를 정의하는 클래스입니다.
#                저희가 만든 파이썬 함수를 LLM 에이전트가 사용할 수 있는 형태로 포장합니다.
from langchain_core.tools import Tool as LangChainTool
# typing (모듈): 파이썬에서 변수나 함수의 입/출력 데이터 '타입'을 명시하는 기능을 제공하는 모듈입니다.
# List (타입): '이 변수는 여러 항목을 담는 목록(리스트)이야'라고 알려줍니다.
# Any (타입): '이 변수는 어떤 종류의 데이터든 될 수 있어'라고 알려줍니다.
from typing import List, Any

# --- 에이전트 작업 공간(Workspace) 설정 ---
# AGENT_WORKSPACE_DIR (변수 - 사용자 정의):
# 에이전트가 파일 시스템 작업을 수행할 '샌드박스(Sandbox)' 디렉토리(폴더)의 경로를 정의하는 변수입니다.
# 이 폴더는 백엔드 프로젝트 루트 (예: project05\backend) 아래에 생성됩니다.
# 이 경로를 변경하여 에이전트가 접근할 수 있는 파일 시스템의 범위를 조절할 수 있습니다.
# 나중에 MCP(Model Context Protocol)와 같은 시스템을 연동할 경우,
# 이 디렉토리가 MCP 파일 시스템 서버가 관리하는 특정 경로와 연결될 수 있습니다.
AGENT_WORKSPACE_DIR = "./agent_workspace"

# if (조건문): 특정 '조건'이 참(True)일 때만 특정 코드 블록을 실행하도록 합니다.
# not (키워드): '조건'의 결과를 반대로 만듭니다. (참이면 거짓으로, 거짓이면 참으로)
# os.path.exists (함수 - 파이썬 내장/모듈 함수): 지정된 경로의 파일이나 폴더가 '존재하는지' 확인하여 참/거짓을 반환합니다.
# os.makedirs (함수 - 파이썬 내장/모듈 함수): 지정된 경로에 폴더를 생성합니다.
if not os.path.exists(AGENT_WORKSPACE_DIR):
    os.makedirs(AGENT_WORKSPACE_DIR)
    # print (함수 - 파이썬 내장): 디버깅 메시지를 콘솔에 출력합니다.
    print(f"[AgentTools DEBUG] Created agent workspace directory: {AGENT_WORKSPACE_DIR}")

# def (키워드): 새로운 '함수(Function)'를 정의할 때 사용하는 키워드입니다.
# _get_safe_path (함수 - 사용자 정의): 함수 이름입니다. (관례적으로 '_'로 시작하는 함수는 내부용으로 사용됩니다.)
# file_path (매개변수): 함수가 외부로부터 받는 입력 값입니다.
# str (타입): file_path가 '문자열(string)' 타입임을 명시합니다.
# -> (타입 힌팅): 함수가 반환하는 값의 타입을 명시합니다.
def _get_safe_path(file_path: str) -> str: 
    """
    주어진 파일 경로가 AGENT_WORKSPACE_DIR 내부에 있는지 확인하고 안전한 절대 경로를 반환합니다.
    이 함수는 에이전트가 정의된 작업 공간을 벗어나 시스템의 다른 파일에 접근하는 것을 방지하는
    핵심적인 보안 장치입니다.
    """
    # os.path.abspath (함수 - 파이썬 내장/모듈 함수): 상대 경로를 절대 경로로 변환합니다.
    base_path = os.path.abspath(AGENT_WORKSPACE_DIR)
    # os.path.join (함수 - 파이썬 내장/모듈 함수): 운영체제에 맞는 경로 구분자(\ 또는 /)를 자동으로 사용하여 경로를 결합합니다.
    abs_path = os.path.abspath(os.path.join(base_path, file_path))
    
    # if (조건문): 생성된 abs_path (변수)가 base_path (변수)로 시작하는지 확인합니다.
    # not (키워드): 조건의 결과를 반대로 만듭니다.
    # .startswith (메서드): 문자열이 특정 문자열로 시작하는지 확인하는 함수입니다.
    if not abs_path.startswith(base_path):
        # raise (키워드): 특정 '예외(오류)'를 강제로 발생시킵니다.
        # ValueError (예외 - 파이썬 내장): 잘못된 값이나 인자가 전달되었을 때 발생하는 표준 예외입니다.
        raise ValueError(f"'{file_path}' is outside the allowed agent workspace.")
    return abs_path

def create_file(file_path: str, content: str = "") -> str: # create_file (함수 - 사용자 정의)
    """
    지정된 경로에 새로운 텍스트 파일을 생성하거나 기존 파일을 덮어씁니다.
    파일은 AGENT_WORKSPACE_DIR 내부에만 생성/수정될 수 있습니다.
    """
    # try (키워드): 특정 코드 블록을 실행해보고, 오류(예외)가 발생하면 except 블록으로 넘어갑니다.
    try:
        safe_path = _get_safe_path(file_path) # _get_safe_path (함수) 호출: 안전한 경로를 확인합니다.
        # os.makedirs (함수 - 파이썬 내장/모듈 함수): 파일이 저장될 상위 디렉토리가 없으면 자동으로 생성합니다.
        # exist_ok=True (매개변수): 폴더가 이미 존재해도 오류를 발생시키지 않습니다.
        os.makedirs(os.path.dirname(safe_path), exist_ok=True) 
        # open (함수 - 파이썬 내장): 파일을 쓰기 모드('w')로 열고 내용을 작성합니다. (UTF-8 인코딩 사용)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"파일 '{file_path}'이(가) 성공적으로 생성/수정되었습니다."
    except ValueError as e: # ValueError (예외 - 파이썬 내장): _get_safe_path에서 발생한 오류를 잡습니다.
        return f"오류: {e}"
    except Exception as e: # Exception (예외 - 파이썬 내장): 그 외 발생할 수 있는 모든 오류를 잡습니다.
        return f"파일 생성/수정 중 오류 발생: {type(e).__name__} - {e}"

def read_file(file_path: str) -> str: # read_file (함수 - 사용자 정의)
    """
    지정된 경로의 텍스트 파일 내용을 읽어 반환합니다.
    파일은 AGENT_WORKSPACE_DIR 내부에 있어야 합니다.
    """
    try:
        safe_path = _get_safe_path(file_path) # _get_safe_path (함수) 호출
        # os.path.exists (함수 - 파이썬 내장/모듈 함수): 파일이 존재하는지 확인합니다.
        if not os.path.exists(safe_path):
            return f"오류: 파일 '{file_path}'이(가) 존재하지 않습니다."
        # open (함수 - 파이썬 내장): 파일을 읽기 모드('r')로 열고 내용을 읽어옵니다.
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"파일 '{file_path}' 내용:\n{content}"
    except ValueError as e: # ValueError (예외 - 파이썬 내장)
        return f"오류: {e}"
    except Exception as e: # Exception (예외 - 파이썬 내장)
        return f"파일 읽기 중 오류 발생: {type(e).__name__} - {e}"

def delete_file(file_path: str) -> str: # delete_file (함수 - 사용자 정의)
    """
    지정된 경로의 파일을 삭제합니다.
    파일은 AGENT_WORKSPACE_DIR 내부에 있어야 합니다.
    """
    try:
        safe_path = _get_safe_path(file_path) # _get_safe_path (함수) 호출
        # os.path.exists (함수 - 파이썬 내장/모듈 함수): 파일이 존재하는지 확인합니다.
        if not os.path.exists(safe_path):
            return f"오류: 파일 '{file_path}'이(가) 존재하지 않습니다."
        # os.remove (함수 - 파이썬 내장/모듈 함수): 파일을 삭제합니다.
        os.remove(safe_path)
        return f"파일 '{file_path}'이(가) 성공적으로 삭제되었습니다."
    except ValueError as e: # ValueError (예외 - 파이썬 내장)
        return f"오류: {e}"
    except Exception as e: # Exception (예외 - 파이썬 내장)
        return f"파일 삭제 중 오류 발생: {type(e).__name__} - {e}"

def list_directory(directory_path: str = ".") -> str: # list_directory (함수 - 사용자 정의)
    """
    지정된 디렉토리의 파일 및 하위 디렉토리 목록을 반환합니다.
    디렉토리는 AGENT_WORKSPACE_DIR 내부에 있어야 하며, _get_safe_path 함수에 의해 검증됩니다.
    기본값은 현재 에이전트 작업 디렉토리(AGENT_WORKSPACE_DIR)의 루트입니다.
    """
    try:
        safe_path = _get_safe_path(directory_path) # _get_safe_path (함수) 호출
        # os.path.isdir (함수 - 파이썬 내장/모듈 함수): 지정된 경로가 디렉토리인지 확인합니다.
        if not os.path.isdir(safe_path):
            return f"오류: '{directory_path}'은(는) 디렉토리가 아닙니다."
        
        # os.listdir (함수 - 파이썬 내장/모듈 함수): 디렉토리 내의 모든 항목(파일 및 폴더) 이름을 가져옵니다.
        items = os.listdir(safe_path)
        # if (조건문): items (변수) 리스트가 비어있는지 확인합니다.
        if not items:
            return f"디렉토리 '{directory_path}'이(가) 비어 있습니다."
        
        # 목록을 문자열로 결합하여 반환합니다.
        return f"디렉토리 '{directory_path}' 내용:\n" + "\n".join(items)
    except ValueError as e: # ValueError (예외 - 파이썬 내장)
        return f"오류: {e}"
    except Exception as e: # Exception (예외 - 파이썬 내장)
        return f"디렉토리 목록 조회 중 오류 발생: {type(e).__name__} - {e}"

# --- LangChain Tool 정의 ---
# 위에서 정의한 파이썬 함수들을 LLM 에이전트가 사용할 수 있는 '도구(Tool)'로 만듭니다.
# 각 '도구'는 이름(name)과 설명(description)을 가지며, LLM이 이 설명을 보고
# 어떤 도구를 언제 사용할지 스스로 판단하게 됩니다.
# 나중에 MCP(Model Context Protocol)와 같은 시스템을 연동할 경우,
# 이러한 도구들이 MCP 서버의 특정 기능(예: filesystem 서버의 'createFile' 액션)과
# 연결되도록 추상화 계층을 추가할 수 있습니다.
file_tools = [ # file_tools (변수 - 사용자 정의): 파일 시스템 도구들의 리스트입니다.
    LangChainTool( # LangChainTool (클래스)
        name="create_file", # name (속성): 도구의 이름 (LLM이 호출할 이름)
        description=""" # description (속성): 도구의 기능 설명 (LLM이 도구 사용 여부를 판단할 때 참고)
        새로운 텍스트 파일을 생성하거나 기존 파일을 덮어씁니다.
        파일은 에이전트의 작업 공간(agent_workspace 폴더) 내부에만 생성/수정될 수 있습니다.
        이 도구를 사용하여 코드를 파일에 저장할 수 있습니다.
        사용 예시: create_file(file_path='my_folder/my_file.txt', content='Hello, world!')
        """,
        func=create_file, # func (속성): 도구가 실행될 때 실제로 호출될 파이썬 함수 (우리가 위에서 정의한 함수)
    ),
    LangChainTool(
        name="read_file",
        description="""
        지정된 텍스트 파일의 내용을 읽어옵니다.
        파일은 에이전트의 작업 공간(agent_workspace 폴더) 내부에 있어야 합니다.
        이 도구를 사용하여 생성된 코드나 다른 파일의 내용을 확인할 수 있습니다.
        사용 예시: read_file(file_path='my_folder/my_file.txt')
        """,
        func=read_file,
    ),
    LangChainTool(
        name="delete_file",
        description="""
        지정된 텍스트 파일을 삭제합니다.
        파일은 에이전트의 작업 공간(agent_workspace 폴더) 내부에 있어야 합니다.
        사용 예시: delete_file(file_path='my_folder/my_file.txt')
        """,
        func=delete_file,
    ),
    LangChainTool(
        name="list_directory",
        description="""
        지정된 디렉토리의 파일 및 하위 디렉토리 목록을 조회합니다.
        디렉토리는 에이전트의 작업 공간(agent_workspace 폴더) 내부에 있어야 합니다.
        기본값은 현재 에이전트 작업 공간의 루트입니다.
        이 도구를 사용하여 에이전트가 작업 공간의 파일 구조를 파악할 수 있습니다.
        사용 예시: list_directory(directory_path='my_folder') 또는 list_directory() (작업 공간 루트)
        """,
        func=list_directory,
    ),
]
