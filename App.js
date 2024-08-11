import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SignupPage from './SignupPage';
import LoginPage from './LoginPage';
import HomePage from './HomePage';
import { WebSocketProvider } from './WebSocket';

import './Style/App.css';

function App() {
  return (
    <WebSocketProvider>
      <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
        </Routes>
      </div>
    </Router> 
    </WebSocketProvider>
  );
}

export default App;