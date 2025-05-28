// frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx'; // 확장자 .tsx 확인
import './index.css';

// 경고 해결: document.getElementById('root')! -> document.getElementById('root') as HTMLElement
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);