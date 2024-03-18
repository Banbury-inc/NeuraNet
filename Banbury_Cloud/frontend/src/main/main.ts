import React, { createContext, useContext, useState } from 'react';
import { app, BrowserWindow, ipcMain } from "electron";
import * as path from "path";
import * as url from "url";
import { exec } from "child_process";
const { spawn } = require("child_process");
import axios from 'axios'; // Adjusted import for axios
import { useStdout } from './StdoutContext';
import { resolve } from 'path';
let mainWindow: BrowserWindow | null;

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1366,
    // frame: false,
    // titleBarStyle: "hidden",
    titleBarOverlay: false,
    height: 768,
    backgroundColor: "#23272a",
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      devTools: process.env.NODE_ENV !== "production",
      preload: path.join(__dirname, 'preload.ts')
    },
  });
 
  const startURL = process.env.NODE_ENV === "development"
    ? "http://localhost:8081"
    : url.format({
        pathname: path.join(__dirname, "index.html"),
        protocol: "file:",
        slashes: true,
      });

  mainWindow.loadURL(startURL);
    // and load the index.html of the app.

//Listen for the 'ready-to-show' event to run the Python script
//  mainWindow.on("ready-to-show", () => {
//    runPythonScript(); // Execute the Python script
//  });



  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}



function runPythonScript() {
  const scriptPath = "src/main/receiver5.py"; // Update this to the path of your Python script
  const python = spawn('python3', [scriptPath]);

  // Listen for data on the stdout stream
  python.stdout.on("data", (data: Buffer) => {
    const result = data.toString();
    console.log(`Python Script Message: ${result}`);

     mainWindow?.webContents.send('python-output', result);
  });

  // Listen for errors on the stderr stream
  python.stderr.on("data", (data: Buffer) => {
    const error = data.toString();
    console.error(`Python Script Error: ${error}`);
  });

  // Handle the exit event
  python.on("close", (code: number) => {
    console.log(`Python Script exited with code ${code}`);
  });

}





// function runPythonScript() {
//   const scriptPath = "src/main/receiver5.py"; // Update this to the path of your Python script
//   exec(`python3 "${scriptPath}"`, (error, stdout, stderr) => {

//     console.log(`Python Script Message: ${stdout}`);
//     console.log(`Python Script Message: ${stderr}`);
//     console.log(`Python Script Message: ${error}`);
//     if (error) {
//       console.error(`exec error: ${error}`);
//       return
//     }
//     if (stderr) {
//       console.error(`Python Script Error: ${stderr}`);
//       return
//     }
//     if (stdout) {
//       console.log(`Python Script Message: ${stdout}`);
//       return
//     }
//     resolve(stdout); 
//     // Example: Send output to renderer process if needed
//      // mainWindow?.webContents.send('python-output', stdout);
//   });
// }

ipcMain.on('fetch-data', async (event, args) => {
  try {
    const response = await axios.get('https://catfact.ninja/fact');
    event.reply('fetch-data-response', response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});

app.on("ready", () => {
  createWindow();
  runPythonScript();


});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
//app.whenReady().then(() => {
//  runPythonScript();
//}
//)



app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});




