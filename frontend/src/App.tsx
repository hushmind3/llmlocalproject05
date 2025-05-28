import { useState, useRef, useEffect } from 'react';
import Sidebar from './Sidebar'; // Sidebar 컴포넌트 임포트

// 메시지 타입을 정의합니다.
interface ChatMessage {
  id: number;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
}

// 세션 제목 타입을 정의합니다.
interface SessionTitle {
  session_id: string;
  title: string;
  timestamp: string;
}

function App() {
  const [messageInput, setMessageInput] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null); // 현재 세션 ID 상태
  const [sessionTitles, setSessionTitles] = useState<SessionTitle[]>([]); // 모든 세션 제목 목록

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // 메시지 목록이 업데이트될 때마다 자동으로 스크롤
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // 컴포넌트 마운트 시 입력 필드에 초기 포커스 설정
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // 모든 세션 제목을 백엔드에서 불러오는 함수
  const fetchSessionTitles = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat/sessions');
      if (!res.ok) {
        throw new Error(`세션 목록 로드 실패: ${res.status}`);
      }
      const data = await res.json();
      setSessionTitles(data.sessions);
      return data.sessions;
    } catch (err) {
      console.error('세션 목록 로드 오류:', err);
      setError(`세션 목록 로드 오류: ${(err as Error).message}`);
      return [];
    }
  };

  // 앱 로드 시 세션 불러오기 또는 새 세션 시작
  useEffect(() => {
    const initializeSession = async () => {
      const titles = await fetchSessionTitles();
      if (titles && titles.length > 0) {
        // 가장 최근 세션을 자동으로 로드합니다.
        await loadSession(titles[0].session_id);
      } else {
        // 저장된 세션이 없으면 새 세션을 시작합니다.
        startNewChat(false); // 처음 로드 시에는 이전 세션을 저장하지 않음
      }
    };
    initializeSession();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // 컴포넌트 마운트 시 한 번만 실행

  // 새 채팅을 시작하는 함수
  const startNewChat = async (saveCurrent: boolean = true) => {
    // 현재 대화 중인 세션이 있고, 저장해야 한다면 먼저 저장합니다.
    if (saveCurrent && currentSessionId && messages.length > 0) {
      // handleSubmit 내부에서 메시지를 저장하므로, 여기서는 UI 초기화만 진행
      // 또는 명시적으로 저장 API 호출 로직 추가 (현재는 handleSubmit에 통합)
    }

    const newId = String(Date.now()) + Math.random().toString(36).substring(2, 9); // 임시 새 세션 ID
    setCurrentSessionId(newId);
    setMessages([]);
    setMessageInput('');
    // setResponse(''); // 응답 필드 없음
    setError(null);
    setLoading(false);
    await fetchSessionTitles(); // 세션 목록 새로고침
  };

  // 특정 세션 로드 함수
  const loadSession = async (sessionId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/chat/session/${sessionId}`);
      if (!res.ok) {
        throw new Error(`세션 로드 실패: ${res.status}`);
      }
      const data = await res.json();
      setMessages(data.messages); // 불러온 메시지로 설정
      setCurrentSessionId(sessionId); // 현재 세션 ID 업데이트
      inputRef.current?.focus(); // 입력 필드 포커스
    } catch (err) {
      console.error('세션 로드 오류:', err);
      setError(`세션 로드 오류: ${(err as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  // 세션 삭제 함수
  const deleteSession = async (sessionId: string) => {
    if (!window.confirm('정말로 이 세션을 삭제하시겠습니까?')) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/chat/session/${sessionId}`, {
        method: 'DELETE',
      });
      if (!res.ok) {
        throw new Error(`세션 삭제 실패: ${res.status}`);
      }
      // 삭제 성공 후 세션 목록 새로고침
      const updatedTitles = await fetchSessionTitles();
      
      // 현재 세션이 삭제되었으면 새 세션으로 전환
      if (currentSessionId === sessionId) {
        if (updatedTitles && updatedTitles.length > 0) {
          await loadSession(updatedTitles[0].session_id); // 가장 최근 세션 로드
        } else {
          startNewChat(false); // 세션이 없으면 새 빈 채팅 시작
        }
      }
    } catch (err) {
      console.error('세션 삭제 오류:', err);
      setError(`세션 삭제 오류: ${(err as Error).message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    const userMessageText = messageInput.trim();
    if (!userMessageText) {
      setError('메시지를 입력해주세요.');
      return;
    }

    setError(null);
    setLoading(true);

    const newUserMessage: ChatMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: userMessageText,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    setMessageInput('');

    try {
      // 세션 ID를 백엔드로 함께 보냅니다.
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessageText, session_id: currentSessionId }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || `HTTP 오류: ${res.status}`);
      }

      const data: { response: string; session_id: string } = await res.json();

      const aiResponse: ChatMessage = {
        id: messages.length + 2,
        sender: 'ai',
        text: data.response,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prevMessages) => [...prevMessages, aiResponse]);
      // 백엔드에서 새로운 세션 ID를 받으면 현재 세션 ID를 업데이트 (새 세션 시작 시)
      if (data.session_id && data.session_id !== currentSessionId) {
        setCurrentSessionId(data.session_id);
      }
      await fetchSessionTitles(); // 세션 목록 새로고침 (새 세션 저장 시 제목 업데이트 위함)

    } catch (err) {
      console.error('백엔드 통신 오류:', err);
      setError(`오류 발생: ${(err as Error).message || '알 수 없는 오류'}. 백엔드 서버가 실행 중인지 확인해주세요.`);
    } finally {
      setLoading(false);
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0);
    }
  };

  return (
    // 전체 화면 컨테이너: 배경색을 흰색 계열로 변경
    <div className="min-h-screen flex bg-gray-50 font-inter text-gray-800 antialiased">
      {/* 사이드바 컴포넌트 배치 */}
      <Sidebar 
        sessionTitles={sessionTitles} 
        onNewChat={startNewChat} 
        onLoadSession={loadSession}
        onDeleteSession={deleteSession}
        currentSessionId={currentSessionId}
      />

      {/* 메인 채팅 컨테이너: 사이드바 옆에 나머지 공간을 채우도록 flex-1 사용 */}
      <div className="flex flex-col flex-1 h-screen bg-white">
        {/* 헤더 영역 */}
        <div className="flex items-center justify-between p-4 bg-white text-gray-800 shadow-md border-b border-gray-200">
          <h1 className="text-xl md:text-2xl font-bold flex items-center">
            <span role="img" aria-label="rocket" className="mr-2 text-3xl">🚀</span> 한국어 AI 코딩 에이전트
          </h1>
        </div>

        {/* 메시지 표시 영역: 스크롤 가능, 양 옆에 여백 추가 (px-4) */}
        <div className="flex-1 px-4 py-6 overflow-y-auto custom-scrollbar bg-white">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className="flex mb-4 justify-start items-start"
            >
              {/* 메시지 아이콘: AI는 🤖, 사용자는 👤 이모티콘으로 */}
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-lg mr-2">
                {msg.sender === 'ai' ? '🤖' : '👤'}
              </div>
              <div
                className={`max-w-[80%] p-3 rounded-lg text-sm md:text-base bg-white`}
              >
                <p className="whitespace-pre-wrap break-words">{msg.text}</p>
                <span className="block text-xs mt-1 text-gray-500 text-left">
                  {msg.timestamp}
                </span>
              </div>
            </div>
          ))}
          {/* 로딩 인디케이터 */}
          {loading && (
            <div className="flex justify-start mb-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-lg mr-2">
                🤖
              </div>
              <div className="max-w-[80%] p-3 rounded-lg bg-white">
                <p className="animate-pulse">생각 중...</p>
              </div>
            </div>
          )}
          {/* 오류 메시지 */}
          {error && (
            <div className="flex justify-start mb-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-red-200 flex items-center justify-center text-lg mr-2">
                ⚠️
              </div>
              <div className="max-w-[80%] p-3 rounded-lg bg-red-100 text-red-700 border border-red-300">
                <p className="text-sm break-words whitespace-pre-wrap">{error}</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 입력 영역: 하단 고정, 흰색 배경, 화살표 아이콘 */}
        <div className="px-4 py-2 bg-white border-t border-gray-200 flex items-center">
          <div className="relative flex-grow">
            <input
              type="text"
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !loading) {
                  handleSubmit();
                }
              }}
              placeholder="무엇을 도와드릴까요?"
              ref={inputRef}
              className="w-full p-3 pr-10 border border-gray-200 rounded-full focus:outline-none focus:ring-0 focus:border-gray-400 text-gray-900"
              disabled={loading}
            />
            <button
              onClick={handleSubmit}
              disabled={loading}
              type="button"
              className="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="메시지 전송"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="currentColor"
                className="w-5 h-5"
              >
                <title>메시지 전송</title>
                <path d="M7 2L17 12L7 22Z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
