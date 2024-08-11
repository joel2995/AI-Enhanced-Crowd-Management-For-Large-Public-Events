import React from 'react';
import ReactDOM from 'react-dom';
import './Style/index.css';
import App from './App';
import { WebSocketProvider } from './WebSocket';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

ReactDOM.render(
  <React.StrictMode>
    <WebSocketProvider>
      <App />
    </WebSocketProvider>
  </React.StrictMode>,
  document.getElementById('root')
); 

reportWebVitals();
