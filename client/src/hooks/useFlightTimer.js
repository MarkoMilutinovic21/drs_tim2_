import { useState, useEffect } from 'react';

// Custom hook for tracking ongoing flight remaining time
// on je hooks zato sto koristi useState/useEffect da promeni nesto
// dok su obicni helperi neke obicne kalkulacije
export const useFlightTimer = (flight) => {
  const [remainingTime, setRemainingTime] = useState(null);
  const [isOngoing, setIsOngoing] = useState(false);

  useEffect(() => {
    if (!flight || !flight.is_ongoing) {
      setIsOngoing(false);
      setRemainingTime(null);
      return;
    }

    setIsOngoing(true);
    setRemainingTime(flight.remaining_time);

    // Update every second
    const interval = setInterval(() => {
      setRemainingTime((prev) => {
        if (prev === null || prev <= 0) {
          setIsOngoing(false);
          return 0;
        }
        return prev - 1;
      });
    }, 60000); // Update every minute - malo glupo ali na 60s odradi -1min

    return () => clearInterval(interval);
  }, [flight]);

  const formatTime = () => {
    if (remainingTime === null) return '--';
    
    const hours = Math.floor(remainingTime / 60);
    const minutes = remainingTime % 60;
    
    return `${hours}h ${minutes}m`;
  };

  return { remainingTime, isOngoing, formatTime };  // ovo koristi flights.jsx 
                                                    // da prikaze tajmer za kartici let
};