import React from 'react';

// Sidebar 컴포넌트의 props 타입을 정의합니다.
interface SidebarProps {
  // 백엔드에서 불러온 세션 제목 목록입니다.
  sessionTitles: { session_id: string; title: string; timestamp: string }[]; 
  // '새 채팅' 버튼 클릭 시 App.tsx에서 호출될 함수입니다.
  onNewChat: () => void; 
  // 과거 세션 목록의 아이템 클릭 시 해당 세션을 로드하기 위해 App.tsx에서 호출될 함수입니다.
  onLoadSession: (sessionId: string) => void; 
  // 세션 삭제 버튼 클릭 시 해당 세션을 삭제하기 위해 App.tsx에서 호출될 함수입니다.
  onDeleteSession: (sessionId: string) => void; 
  // 현재 활성화된 세션의 ID입니다. 사이드바에서 현재 세션을 시각적으로 강조하는 데 사용됩니다.
  currentSessionId: string | null; 
}

// Sidebar 컴포넌트 정의
function Sidebar({ sessionTitles, onNewChat, onLoadSession, onDeleteSession, currentSessionId }: SidebarProps) {
  return (
    // 사이드바 컨테이너: 고정 너비, 전체 높이, 흰색 배경, 어두운 텍스트, 그림자, 오른쪽 테두리
    <div className="flex flex-col w-64 h-screen bg-white text-gray-800 shadow-lg border-r border-gray-100">
      {/* 사이드바 헤더 */}
      <div className="p-4 border-b border-gray-200 flex items-center">
        {/* 캐릭터 아이콘 SVG (이전 대화에서 추가된 아이콘) */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-6 h-6 text-blue-500" 
        >
          <title>캐릭터 아이콘</title>
          <circle cx="12" cy="10" r="4" />
          <path d="M17.24 16.5c-.38-2.1-2.05-3.8-4.24-4.5-2.19-.7-4.56-.7-6.75 0-2.19.7-3.86 2.4-4.24 4.5-.07.4.24.8.64.8h13.2c.4 0 .71-.4.64-.8z" />
        </svg>
        <h2 className="text-xl font-bold ml-2">챗 에이전트</h2>
      </div>

      {/* 새 채팅 버튼 */}
      <div className="p-4">
        <button
          onClick={onNewChat} // '새 채팅' 버튼 클릭 시 App.tsx에서 전달받은 onNewChat 함수 호출
          className="w-full py-2 px-4 rounded-md bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold flex items-center justify-center space-x-2 transition-colors duration-200 border border-gray-200"
          type="button"
          aria-label="새 채팅 시작"
        >
          {/* 새 채팅 아이콘 */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <title>새 채팅</title>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          <span>새 채팅</span>
        </button>
      </div>

      {/* 채팅 세션 목록 영역 */}
      <div className="flex-1 p-4 overflow-y-auto custom-scrollbar">
        <h3 className="text-sm font-semibold text-gray-500 mb-2">과거 세션</h3>
        <ul className="space-y-2">
          {sessionTitles.length === 0 ? (
            // 저장된 세션이 없을 경우 표시되는 메시지
            <li className="text-gray-500 text-sm">저장된 세션이 없습니다.</li>
          ) : (
            // sessionTitles 배열을 순회하며 각 세션 아이템을 렌더링합니다.
            sessionTitles.map((session) => (
              <li
                key={session.session_id}
                // 현재 활성화된 세션과 일치하면 다른 배경색으로 강조합니다.
                className={`group flex items-center justify-between p-2 rounded-md cursor-pointer transition-colors duration-200 
                            ${currentSessionId === session.session_id ? 'bg-blue-100 text-blue-800 font-semibold' : 'hover:bg-gray-100 text-gray-700'}`}
              >
                {/* 세션 제목 표시: 클릭 시 해당 세션을 로드하고, 제목이 길면 ...으로 자릅니다. */}
                <span 
                  className="truncate flex-1" 
                  onClick={() => onLoadSession(session.session_id)}
                  title={session.title} // 마우스 오버 시 전체 제목 표시
                >
                  {session.title || '제목 없음'} {/* 제목이 없으면 '제목 없음' 표시 */}
                </span>
                {/* 세션 삭제 버튼 */}
                <button
                  onClick={(e) => {
                    e.stopPropagation(); // 부모 li의 클릭 이벤트가 발생하지 않도록 막습니다.
                    onDeleteSession(session.session_id); // 세션 삭제 함수 호출
                  }}
                  className={`flex-shrink-0 ml-2 p-1 rounded-full text-gray-400 hover:text-red-500 hover:bg-red-100 
                              ${currentSessionId === session.session_id ? 'visible' : 'invisible group-hover:visible'}`} // 현재 세션이거나 li에 호버 시 보이게
                  type="button"
                  aria-label="세션 삭제"
                >
                  {/* 삭제 아이콘 (X 모양) */}
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                    <title>세션 삭제</title>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </li>
            ))
          )}
        </ul>
      </div>

      {/* 설정/기타 링크 (하단 고정) */}
      <div className="p-4 border-t border-gray-200">
        <a 
          href="javascript:void(0)" // 클릭 시 페이지 이동 없는 링크
          className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 transition-colors duration-200"
        >
          {/* 설정 아이콘 */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <title>설정</title>
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0M3.75 18H7.5m-9-6h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0M3.75 12H7.5" />
          </svg>
          <span>설정</span>
        </a>
      </div>
    </div>
  );
}

export default Sidebar;
