import { createContext, useState, useEffect, useContext } from 'react';
import { io } from 'socket.io-client';
import { useAuth } from './AuthContext';

const SocketContext = createContext(null);

const FLIGHT_SERVICE_URL = 'http://localhost:5001';

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    if (isAuthenticated()) {
      // Connect to Flight Service WebSocket
      const newSocket = io(FLIGHT_SERVICE_URL, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
      });

      newSocket.on('connect', () => {
        console.log('Connected to Flight Service WebSocket');
        setConnected(true);
      });

      newSocket.on('disconnect', () => {
        console.log('Disconnected from Flight Service WebSocket');
        setConnected(false);
      });

      // Listen for new flight notifications (for admin)
      newSocket.on('new_flight', (flightData) => {
        console.log('New flight notification:', flightData);
        addNotification({
          type: 'new_flight',
          message: `New flight created: ${flightData.name}`,
          data: flightData,
          timestamp: new Date().toISOString()
        });
      });

      setSocket(newSocket);

      return () => {
        newSocket.disconnect();
      };
    }
  }, [isAuthenticated()]);

  const addNotification = (notification) => {
    setNotifications((prev) => [notification, ...prev].slice(0, 50)); // Keep last 50
  };

  const clearNotifications = () => {
    setNotifications([]);
  };

  const removeNotification = (index) => {
    setNotifications((prev) => prev.filter((_, i) => i !== index));
  };

  const value = {
    socket,
    connected,
    notifications,
    addNotification,
    clearNotifications,
    removeNotification
  };

  return <SocketContext.Provider value={value}>{children}</SocketContext.Provider>;
};

export const useSocket = () => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error('useSocket must be used within SocketProvider');
  }
  return context;
};