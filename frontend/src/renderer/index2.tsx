import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import Login from "./components/Login";
import axios from 'axios';
import * as fs from 'fs/promises';
import * as path from 'path';
import App from './components/App';


const rootElement = document.getElementById("root");
if (rootElement) {
  const root = createRoot(rootElement);

  interface LoginResponse {
      response: 'success' | 'fail';
      reason?: string; // Making response field optional
  }

  async function authenticate(username: string, password: string): Promise<boolean> {
      try {
          const response = await axios.post<LoginResponse>('https://website2-v3xlkt54dq-uc.a.run.app/login_api/', {
              username,
              password,
          }, {
              headers: {
                  'Content-Type': 'application/json',
              },
          });
   
          if (response.data.response === 'success') {
              console.log('Login successful');

              return true;
          } else {
              console.error('Login failed', response.data.reason);
              return false;
          }
      } catch (error) {
          console.error('Authentication error:', error);
          return false;
      }
  }
   
  function Main() {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
        (async () => {
            const credentials = await fetchCredentials();

            if (credentials === null) {
                // If credentials are not found, directly render the Login component
                root.render(<Login />);
            } else {
                const success = await authenticate(credentials.username, credentials.password);
                setIsAuthenticated(success);
            }
        })();
    }, []);
  
    if (isAuthenticated === null) {
        return <div>Loading...</div>;
    }
    return isAuthenticated ? <App /> : <Login />;
}
   
  root.render(<Main />);
} else {
  console.error("Failed to find the root element");
}

interface Credentials {
  username: string;
  password: string;
}

async function fetchCredentials(): Promise<Credentials | null> {
  try {
    const credentialsPath = path.join(__dirname, '.banbury', 'credentials.json');

    // Check if the file exists
    try {
      await fs.access(credentialsPath);
    } catch (accessError) {
      // If the file doesn't exist, create it with default credentials
      await fs.mkdir(path.dirname(credentialsPath), { recursive: true });
      await fs.writeFile(credentialsPath, JSON.stringify({ username: 'default', password: 'default' }));
    }

    // Read the file
    const data = await fs.readFile(credentialsPath, 'utf8');
    if (!data.trim()) {
      console.error('Credentials file is empty');
      return null;
    }
    const credentialsObj = JSON.parse(data);

    const [username, password] = Object.entries(credentialsObj)[0];

    const credentials: Credentials = { username, password: password as string };

    console.log(credentials);
    return credentials;
  } catch (error: any) {
    console.error('Failed to read credentials:', error);
    return null;
  }
}



export * from "./components/signup";
