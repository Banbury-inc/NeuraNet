import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  username: string | null;
  setUsername: (username: string | null) => void;
  isAuthenticated: boolean; // Change the type to boolean directly
  redirect_to_login: boolean;
  setredirect_to_login: (redirect_to_login: boolean) => void;
  run_receiver: boolean;
  setrun_receiver: (run_receiver: boolean) => void;


}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [username, setUser] = useState<string | null>(null);
  const [redirect_to_login, setredirect_to_login] = useState<boolean>(false); // Add redirect_to_login state
  const [run_receiver, setrun_receiver] = useState<boolean>(false); // Add redirect_to_login state

  const setUsername = (username: string | null) => {
    setUser(username);
  };

  const isAuthenticated = !!username;

  return (
    <AuthContext.Provider value={{ 
      username,
      setUsername, 
      isAuthenticated,
      redirect_to_login,
      setredirect_to_login,
      run_receiver,
      setrun_receiver,

    }}>
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

