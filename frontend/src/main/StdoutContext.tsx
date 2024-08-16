import React, { createContext, useContext, useState } from 'react';

interface StdoutContextType {
  stdoutData: string;
  setStdout: (data: string) => void;
}

const StdoutContext = createContext<StdoutContextType>({ stdoutData: '', setStdout: (data: string) => {} });

export const useStdout = () => useContext(StdoutContext);

export const StdoutProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [stdoutData, setStdoutData] = useState('');

  const setStdout = (data: string) => {
    setStdoutData(data);
  };

  return (
    <StdoutContext.Provider value={{ stdoutData, setStdout }}>
      {children}
    </StdoutContext.Provider>
  );
};
