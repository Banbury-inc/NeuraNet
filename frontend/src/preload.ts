import { contextBridge, ipcRenderer } from 'electron';
import { exec } from 'child_process';


// const { BrowserWindow } = require('@electron/remote')

// Function to run the Python script and capture its output
const runPythonScript = (scriptPath: string): Promise<string> => {
    return new Promise((resolve, reject) => {
        exec(`python ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                reject(`Error executing script: ${error.message}`);
                return;
            }
            if (stderr) {
                reject(`Script error: ${stderr}`);
                return;
            }
            resolve(stdout);
        });
    });
};

const mainProcess = require('electron').ipcRenderer;

async function fetchData() {
  const API_URL = 'https://api.example.com/data';
  mainProcess.send('fetch-data', API_URL);
  mainProcess.once('fetch-data-response', (event, data) => {
    // Use the fetched data here
    console.log(data);
  });
  mainProcess.once('fetch-data-error', (event, errorMessage) => {
    console.error('Error fetching data:', errorMessage);
    // Handle errors gracefully, e.g., display an error message to the user
  });
}

fetchData();


contextBridge.exposeInMainWorld('electronAPI', {
    receivePythonOutput: (callback: (output: string) => void) => {
        ipcRenderer.on('python-output', (_, output) => callback(output));
    },
});

