# model.py

# from (키워드): 특정 모듈(라이브러리) 안에서 특정 부분(클래스, 함수 등)만 선택적으로 가져올 때 사용합니다.
# import (키워드): 다른 파이썬 파일이나 라이브러리(모듈)에 있는 기능을 현재 파일로 가져올 때 사용합니다.
# langchain_ollama (모듈): LangChain 라이브러리에서 Ollama 관련 기능을 제공하는 모듈입니다.
# ChatOllama (클래스): Ollama 서버에서 실행되는 LLM과 파이썬 코드가 상호작용할 수 있도록 해주는 클래스입니다.
#                       이 클래스는 LangGraph가 LLM을 호출할 때 사용하는 '도구' 역할을 합니다.
from langchain_ollama import ChatOllama
# OllamaEmbeddings (클래스): LangChain 라이브러리에서 Ollama 임베딩 모델과 상호작용하는 클래스입니다.
#                            RAG(검색 증강 생성) 기능을 위해 문서 텍스트를 숫자 벡터로 변환하는 데 사용됩니다.
from langchain_ollama import OllamaEmbeddings
# typing (모듈): 파이썬에서 변수나 함수의 입/출력 데이터 '타입'을 명시하는 기능을 제공하는 모듈입니다.
# Any (타입): '이 변수는 어떤 종류의 데이터든 될 수 있어'라고 알려줍니다.
# Optional (타입): '이 변수는 지정된 타입이거나 None(값이 없음)일 수 있어'라고 알려줍니다.
# Tuple (타입): '이 변수는 여러 항목을 순서대로 담는 튜플이야'라고 알려줍니다.
from typing import Any, Optional, Tuple

# --- LLM 및 임베딩 모델 설정값 정의 ---
# OLLAMA_LLM_MODEL_NAME (변수 - 사용자 정의):
# 사용할 LLM(대규모 언어 모델)의 이름을 정의합니다. 이 모델은 Ollama 서버에 미리 다운로드되어 있어야 합니다.
# 예: 'ollama run aroxima/eeve-korean_instruct-10.8b-expo:latest'
OLLAMA_LLM_MODEL_NAME = "aroxima/eeve-korean_instruct-10.8b-expo:latest" 
# OLLAMA_EMBEDDING_MODEL_NAME (변수 - 사용자 정의):
# 사용할 임베딩 모델의 이름을 정의합니다. RAG를 위해 텍스트를 숫자 벡터로 변환하는 데 사용됩니다.
# 이 모델은 Ollama 서버에 미리 다운로드되어 있어야 합니다.
# 예: 'ollama run daynice/kure-v1:latest'
OLLAMA_EMBEDDING_MODEL_NAME = "daynice/kure-v1:latest" 
# OLLAMA_BASE_URL (변수 - 사용자 정의):
# Ollama 서버의 기본 URL을 정의합니다. 일반적으로 로컬에서 Ollama가 실행되는 주소를 가리킵니다.
OLLAMA_BASE_URL = "http://localhost:11434"
# OLLAMA_REQUEST_TIMEOUT (변수 - 사용자 정의):
# Ollama 서버에 요청을 보낼 때의 최대 대기 시간(초)을 정의합니다. 이 시간 안에 응답이 없으면 타임아웃 오류가 발생합니다.
OLLAMA_REQUEST_TIMEOUT = 120.0

# async (키워드): 이 함수가 비동기적으로 실행될 수 있음을 나타냅니다. (다른 작업을 기다리지 않고 동시에 진행 가능)
# def (키워드): 새로운 '함수(Function)'를 정의할 때 사용하는 키워드입니다.
# load_llm_and_embedding_instance (함수 - 사용자 정의): 함수 이름입니다.
# -> (타입 힌팅): 함수가 반환하는 값의 타입을 명시합니다.
async def load_llm_and_embedding_instance() -> Tuple[Optional[ChatOllama], Optional[OllamaEmbeddings]]:
    """
    Ollama 서버에서 LLM(대규모 언어 모델)과 임베딩 모델 인스턴스를 로드하는 비동기 함수입니다.
    성공 시 (ChatOllama 인스턴스, OllamaEmbeddings 인스턴스) 튜플을 반환하고, 실패 시 (None, None)을 반환합니다.
    """
    # llm (변수 - 사용자 정의): LLM 인스턴스를 저장할 변수입니다. 초기에는 값이 없습니다(None).
    llm = None
    # embed_model (변수 - 사용자 정의): 임베딩 모델 인스턴스를 저장할 변수입니다. 초기에는 값이 없습니다(None).
    embed_model = None
    # try (키워드): 특정 코드 블록을 실행해보고, 오류(예외)가 발생하면 except 블록으로 넘어갑니다.
    try:
        # ChatOllama (클래스): LLM 인스턴스를 생성합니다.
        # model (속성): 사용할 LLM 모델 이름 (OLLAMA_LLM_MODEL_NAME 변수 값 사용).
        # base_url (속성): Ollama 서버 주소 (OLLAMA_BASE_URL 변수 값 사용).
        # request_timeout (속성): 요청 타임아웃 (OLLAMA_REQUEST_TIMEOUT 변수 값 사용).
        llm = ChatOllama(
            model=OLLAMA_LLM_MODEL_NAME,
            base_url=OLLAMA_BASE_URL,
            request_timeout=OLLAMA_REQUEST_TIMEOUT
        )
        # OllamaEmbeddings (클래스): 임베딩 모델 인스턴스를 생성합니다.
        # model (속성): 사용할 임베딩 모델 이름 (OLLAMA_EMBEDDING_MODEL_NAME 변수 값 사용).
        # base_url (속성): Ollama 서버 주소 (OLLAMA_BASE_URL 변수 값 사용).
        embed_model = OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL_NAME,
            base_url=OLLAMA_BASE_URL
        )
        # return (키워드): 함수의 실행을 종료하고 값을 반환합니다.
        # Tuple (타입): LLM 인스턴스와 임베딩 모델 인스턴스를 튜플 형태로 함께 반환합니다.
        return llm, embed_model 
    # except (키워드): try 블록에서 오류(예외)가 발생했을 때 실행될 코드 블록을 정의합니다.
    # Exception (예외 - 파이썬 내장): 모든 종류의 일반적인 오류를 잡습니다.
    # as (키워드): 발생한 오류 객체를 'e'라는 변수에 할당합니다.
    except Exception as e:
        # None (값): '값이 없음'을 나타내는 파이썬의 특별한 값입니다.
        # Tuple (타입): LLM 로딩 실패 시 (None, None) 튜플을 반환합니다.
        return None, None 
