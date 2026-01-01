import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css' // ⚠️ هذا السطر هو المسؤول عن تحويل الشاشة للسواد والتصميم

const rootElement = document.getElementById('root');

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("عنصر root مفقود!");
}