# main.py
import uvicorn
from server import app # server.py에서 정의된 FastAPI 앱 인스턴스를 임포트합니다.

# 서버 실행 (스크립트로 직접 실행 시)
if __name__ == "__main__":
    # server.py에서 정의된 'app' 인스턴스를 Uvicorn으로 실행합니다.
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
