import React from 'react'; // 'React'가 사용되지 않으므로 제거합니다.

// Sidebar 컴포넌트 정의
function Sidebar() {
  return (
    // 사이드바 컨테이너: 배경색을 흰색으로 변경, 텍스트 색상도 어둡게 변경, 그림자 유지
    <div className="flex flex-col w-64 h-screen bg-white text-gray-800 shadow-lg border-r border-gray-100"> {/* bg-gray-800 -> bg-white, text-white -> text-gray-800, 옅은 회색 테두리 추가 */}
      {/* 사이드바 헤더 */}
      <div className="p-4 border-b border-gray-200"> {/* border-gray-700 -> border-gray-200로 더 연하게 */}
        <h2 className="text-xl font-bold">챗 에이전트</h2>
      </div>

      {/* 새 채팅 버튼 */}
      <div className="p-4">
        <button
          className="w-full py-2 px-4 rounded-md bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold flex items-center justify-center space-x-2 transition-colors duration-200 border border-gray-200" // 배경색, 텍스트색 변경, 테두리 추가
          type="button"
          aria-label="새 채팅 시작"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <title>새 채팅</title> {/* 오류 해결: SVG 아이콘 설명 추가 */}
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          <span>새 채팅</span>
        </button>
      </div>

      {/* 채팅 세션 목록 (플레이스홀더) */}
      <div className="flex-1 p-4 overflow-y-auto custom-scrollbar">
        <h3 className="text-sm font-semibold text-gray-500 mb-2">과거 세션</h3> {/* 텍스트 색상 조정 */}
        {/* 실제 세션 목록은 여기에 동적으로 렌더링될 수 있습니다. */}
        <ul className="space-y-2">
          <li className="p-2 rounded-md hover:bg-gray-100 cursor-pointer text-sm text-gray-700"> {/* 호버 색상, 텍스트 색상 조정 */}
            <span className="truncate block"># LLM 구조 설명</span>
          </li>
          <li className="p-2 rounded-md hover:bg-gray-100 cursor-pointer text-sm text-gray-700">
            <span className="truncate block"># 프론트엔드 UI 수정</span>
          </li>
          {/* 더 많은 세션 아이템... */}
        </ul>
      </div>

      {/* 설정/기타 링크 (하단 고정) */}
      <div className="p-4 border-t border-gray-200"> {/* border-gray-700 -> border-gray-200로 더 연하게 */}
        <a 
          href="javascript:void(0)" // 오류 해결: href="#" 대신 "javascript:void(0)" 사용
          className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 transition-colors duration-200"
        >
          {/* SVG 아이콘에 title 요소 추가 (접근성 오류 해결) */}
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <title>설정</title> {/* 오류 해결: SVG 아이콘 설명 추가 */}
            <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0M3.75 18H7.5m-9-6h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0M3.75 12H7.5" />
          </svg>
          <span>설정</span>
        </a>
      </div>
    </div>
  );
}

export default Sidebar;
