import { useState, useEffect } from 'react';

export const useRealTime = (updateInterval = 3000) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [updateIndex, setUpdateIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      setUpdateIndex(prev => prev + 1);
    }, updateInterval);

    return () => clearInterval(timer);
  }, [updateInterval]);

  return { currentTime, updateIndex };
};