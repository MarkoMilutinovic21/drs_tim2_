import { createContext, useState, useEffect, useContext } from 'react';
import { io } from 'socket.io-client';
import { useAuth } from './AuthContext';

const SocketContext = createContext(null);

const FLIGHT_SERVICE_URL = 'http://localhost:5001';

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [serverSocket, setServerSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const { isAuthenticated, refreshUser, user } = useAuth();
  const SERVER_URL = 'http://localhost:5000';

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

      // Connect to Server WebSocket (role updates)
      const newServerSocket = io(SERVER_URL, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
      });

      newServerSocket.on('role_changed', (payload) => {
        if (payload?.user_id && user?.id === payload.user_id) {
          refreshUser();
        }
      });

      setServerSocket(newServerSocket);

      return () => {
        newSocket.disconnect();
        newServerSocket.disconnect();
      };
    }
  }, [isAuthenticated(), user?.id]);

  const addNotification = (notification) => {
    const id = `${Date.now()}_${Math.random().toString(16).slice(2)}`;
    const next = { id, ...notification };
    setNotifications((prev) => [next, ...prev].slice(0, 50));

    // Dismiss when user explicitly clears (no auto-dismiss here)
  };

  const clearNotifications = () => {
    setNotifications([]);
  };

  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((item) => item.id !== id));
  };

  const value = {
    socket,
    serverSocket,
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
