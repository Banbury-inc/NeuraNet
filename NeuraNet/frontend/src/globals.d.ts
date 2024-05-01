
// src/globals.d.ts or src/types/globals.d.ts
export {}; // This line is necessary if you're using the `declare global` syntax in a module.




declare global {
  namespace NodeJS {
    interface Global {
      GlobalUsername: string | null;
    }
  }


  interface Window {
    electronAPI: {
      onPythonOutput: (callback: (output: string) => void) => void;
      // Declare other methods of electronAPI here if you have more
    };
  }
}
