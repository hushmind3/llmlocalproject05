import { useState, useRef, useEffect } from 'react';
import Sidebar from './Sidebar'; // Sidebar 컴포넌트 임포트

// 메시지 타입을 정의합니다. 사용자 메시지와 AI 응답을 구분합니다.
interface ChatMessage {
  id: number; // 메시지 고유 ID
  sender: 'user' | 'ai'; // 발신자: 사용자 또는 AI
  text: string; // 메시지 내용
  timestamp: string; // 메시지 전송 시간
}

function App() {
  const [messageInput, setMessageInput] = useState<string>(''); // 사용자 입력 필드 상태
  const [messages, setMessages] = useState<ChatMessage[]>([]); // 모든 채팅 메시지 목록
  const [loading, setLoading] = useState<boolean>(false); // 로딩 상태
  const [error, setError] = useState<string | null>(null); // 오류 메시지 상태

  // 메시지 목록이 업데이트될 때 자동으로 스크롤하기 위한 ref
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // 입력 필드에 포커스를 유지하기 위한 ref 추가
  const inputRef = useRef<HTMLInputElement>(null);

  // 메시지 목록이 업데이트될 때마다 자동으로 스크롤
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]); // messages 배열이 변경될 때마다 훅 실행 (자동 스크롤 유지)

  // 컴포넌트 마운트 시 입력 필드에 초기 포커스 설정
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // 메시지 전송 핸들러
  const handleSubmit = async () => {
    const userMessageText = messageInput.trim();
    if (!userMessageText) {
      setError('메시지를 입력해주세요.');
      return;
    }

    setError(null); // 이전 오류 초기화
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
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessageText }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || `HTTP 오류: ${res.status}`);
      }

      const data: { response: string } = await res.json();

      const aiResponse: ChatMessage = {
        id: messages.length + 2, // 사용자 메시지 다음 ID
        sender: 'ai',
        text: data.response,
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prevMessages) => [...prevMessages, aiResponse]);
    } catch (err) {
      console.error('백엔드 통신 오류:', err);
      setError(`오류 발생: ${(err as Error).message || '알 수 없는 오류'}. 백엔드 서버가 실행 중인지 확인해주세요.`);
    } finally {
      setLoading(false); // 로딩 종료
      // 메시지 전송 후 입력 필드에 다시 포커스
      // setTimeout을 사용하여 DOM 업데이트 후 포커스가 확실히 가도록 합니다.
      setTimeout(() => {
        inputRef.current?.focus();
      }, 0); // 0ms 지연은 다음 이벤트 루프 틱에 실행됨을 의미
    }
  };

  // AI 아이콘을 🤖 이모티콘으로 다시 변경합니다.
  // 이제 별도의 AiFaceIcon 컴포넌트 정의는 필요 없습니다.

  return (
    // 전체 화면 컨테이너: 배경색을 흰색 계열로 변경
    <div className="min-h-screen flex bg-gray-50 font-inter text-gray-800 antialiased">
      {/* 사이드바 컴포넌트 배치 */}
      <Sidebar />

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
              // inputRef를 input 요소에 연결
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
