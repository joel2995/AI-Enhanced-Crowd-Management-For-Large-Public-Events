// src/WebSocket.js
import React, { createContext, useContext, useEffect, useState } from 'react';

const WebSocketContext = createContext();

export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new WebSocket('ws://localhost:8080');
    setSocket(ws);

    /*ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onclose = () => {
      //console.log('WebSocket disconnected');
      setIsConnected(false);
    };*/

    ws.onmessage = (event) => { 
      setMessage(event.data);
    };

    // Cleanup on component unmount
    return () => {
      ws.close();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={{ socket, message }}>
      {children}
    </WebSocketContext.Provider>
  );
};

  export const useWebSocket = () => {
    return useContext(WebSocketContext);
};