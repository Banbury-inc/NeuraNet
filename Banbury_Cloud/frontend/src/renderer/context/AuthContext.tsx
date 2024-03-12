// Import necessary modules
import React, { createContext, useState, useContext, ReactNode } from 'react';

// Define the type for the AuthContext
type AuthContextType = {
  username: string | null;
  setUsername: React.Dispatch<React.SetStateAction<string | null>>;
};

// Create the AuthContext
const AuthContext = createContext<AuthContextType>({
  username: null,
  setUsername: () => {},
});

// Create the AuthProvider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [username, setUsername] = useState<string | null>(null);

  return (
    <AuthContext.Provider value={{ username, setUsername }}>
      {children}
    </AuthContext.Provider>
  );
};

// Create a custom hook to access the AuthContext
export const useAuth = () => useContext(AuthContext);

