import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";
import Login from "./components/Login";

import axios from 'axios';

const rootElement = document.getElementById("root");
if (rootElement) {
  const root = createRoot(rootElement);

  interface LoginResponse {
      response: 'success' | 'fail';
      reason?: string; // Include other fields from the response as needed
  }

  // Renamed to `authenticate` to match the usage in the Main component
  async function authenticate(username: string, password: string): Promise<boolean> {
      try {
          const response = await axios.post<LoginResponse>('https://website2-v3xlkt54dq-uc.a.run.app/login_api/', {
          // const response = await axios.post<LoginResponse>('http://0.0.0.0:8080/login_api/', {
              username,
              password,
          }, {
              headers: {
                  'Content-Type': 'application/json',
              },
          });
   
          // Check if login was successful
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
              // Assuming fetchCredentials is a dummy/placeholder function
              const credentials = await fetchCredentials(); // You should define or import this function
              const success = await authenticate(credentials.username, credentials.password);
              setIsAuthenticated(success);
          })();
      }, []);

      if (isAuthenticated === null) {
          return <div>Loading...</div>; // or any other loading indicator
      }
  
      return isAuthenticated ? <App /> : <Login />;
  }
   
  // Render the Main component
  root.render(<Main />);
} else {
  console.error("Failed to find the root element");
}

// Utility function (needs to be defined or imported)
async function fetchCredentials() {
  // Here, you would fetch or read your credentials
  // For demonstration, returning a mock object
  return { username: "mmills6060", password: "Dirtballer6060" };
}

