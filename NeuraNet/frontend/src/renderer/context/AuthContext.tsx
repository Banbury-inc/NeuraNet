import React, { createContext, useContext, useState, ReactNode } from 'react';

interface AuthContextType {
  username: string | null;
  password: string | null;
  first_name: string | null;
  last_name: string | null;
  updates: number;
  devices: any[] | null;
  fileRows: any[];
  global_file_path: string | null;
  global_file_path_device: string | null;
  setUsername: (username: string | null) => void;
  setUpdates: (updates: number) => void;
  setPassword: (password: string | null) => void;
  setFirstname: (first_name: string | null) => void;
  setLastname: (last_name: string | null) => void;
  setGlobal_file_path: (global_file_path: string | null) => void;
  setGlobal_file_path_device: (global_file_path_device: string | null) => void;
  setFileRows: (fileRows: any[]) => void;
  setDevices: (devices: any[] | null) => void;
  isAuthenticated: boolean; // Change the type to boolean directly
  redirect_to_login: boolean;
  setredirect_to_login: (redict_to_login: boolean) => void;
  run_receiver: boolean
  files_is_loading: boolean
  setrun_receiver: (run_receiver: boolean) => void;
  setFilesIsLoading: (files_is_loading: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [username, setUser] = useState<string | null>(null);
  const [password, setPass] = useState<string | null>(null);
  const [first_name, setFirst] = useState<string | null>(null);
  const [last_name, setLast] = useState<string | null>(null);
  const [updates, setUp] = useState<number>(1);
  const [devices, setDev] = useState<any[] | null>(null);
  const [fileRows, setFiles] = useState<any[]>([]);
  const [global_file_path, setFile] = useState<string | null>(null);
  const [global_file_path_device, setFile_Device] = useState<string | null>(null);
  const [redirect_to_login, setredirect_to_login] = useState<boolean>(false); // Add redirect_to_login state
  const [run_receiver, setrun_receiver] = useState<boolean>(false); // Add redirect_to_login state
  const [files_is_loading, setFilesIsLoading] = useState<boolean>(false); // Add redirect_to_login state

  const setUsername = (username: string | null) => {
    setUser(username);
  };
  const setPassword = (password: string | null) => {
    setPass(password);
  };
  const setFirstname = (first_name: string | null) => {
    setFirst(first_name);
  };
  const setGlobal_file_path = (global_file_path: string | null) => {
    setFile(global_file_path);
  };
  const setGlobal_file_path_device = (global_file_path_device: string | null) => {
    setFile_Device(global_file_path_device);
  };
  const setLastname = (last_name: string | null) => {
    setLast(last_name);
  };
  const setUpdates = (updates: number) => {
    setUp(updates);
  };
  const setDevices = (devices: any[] | null) => {
    setDev(devices);
  };
  const setFileRows = (fileRows: any[] | []) => {
    setFiles(fileRows);
  };





  const isAuthenticated = !!username;

  return (
    <AuthContext.Provider value={{
      username,
      password,
      first_name,
      last_name,
      devices,
      fileRows,
      global_file_path,
      global_file_path_device,
      files_is_loading,
      updates,
      setUsername,
      setPassword,
      setFirstname,
      setLastname,
      setDevices,
      setFileRows,
      setGlobal_file_path,
      setUpdates,
      setGlobal_file_path_device,
      setFilesIsLoading,
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

