import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  username: string | null;
  setUsername: (username: string | null) => void;
  isAuthenticated: boolean; // Change the type to boolean directly
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [username, setUser] = useState<string | null>(null);

  const setUsername = (username: string | null) => {
    setUser(username);
  };

  const isAuthenticated = !!username; // Update isAuthenticated to directly return the boolean value

  return (
    <AuthContext.Provider value={{ username, setUsername, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

