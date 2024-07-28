import { Box, CssBaseline, rgbToHex, ThemeProvider } from "@mui/material";
import React, { useEffect, useState } from "react";
import theme from "../theme";
import PermanentDrawerLeft from "./Drawer";
import MiniDrawer from "./VariantDrawer";
import { BrowserRouter, Route, Routes, Outlet, Navigate } from "react-router-dom";
import Signup from "./signup";
import Signin from "./Login";
import Main from "./main";
import { AuthProvider } from "../context/AuthContext";
import Settings from "./Settings";
import Profile from "./Profile";
import TitleBar from 'frameless-titlebar';
import { BrowserWindow } from 'electron';

// Define the Platform type
type Platform = 'win32' | 'linux' | 'darwin';


const DarwinTheme: TitleBarTheme = {

  platform: 'darwin', // Specify the platform ('win32', 'linux', 'darwin')
  bar: {
    palette: 'dark', // Choose between 'light' or 'dark'
    height: '42px', // Set the bar height
    // background: '#171717', // Slightly lighter for elements considered "paper"
    background: '#212121', // Slightly lighter for elements considered "paper"
    // background: '#24292e', // Slightly lighter for elements considered "paper"
    color: '#fff', // White text color
    borderBottom: 'solid #424242', // Slightly darker border at the bottom
    fontFamily: 'inherit', // Font family for the title bar text
    title: {
      align: 'center', // Align the title text to the left
      color: 'inherit', // White title text color
    },
  },
  menu: {
    palette: 'dark',
    style: 'default', // Use the default menu style
    separator: {
      color: '#444', // Color for separators in the menu
    },
  },
  controls: {
    layout: 'right',
    normal: {
      default: { background: 'transparent', color: 'transparent' },
      hover: { background: 'transparent', color: 'transparent' },
    },
    close: {
      default: { background: 'transparent', color: 'transparent' },
      hover: { background: 'transparent', color: 'transparent' },
    },
  },

};


const linuxTheme: TitleBarTheme = {
  platform: 'linux', // Specify the platform ('win32', 'linux', 'darwin')
  bar: {
    palette: 'dark', // Choose between 'light' or 'dark'
    height: '42px', // Set the bar height
    background: '#212121', // Slightly lighter for elements considered "paper"
    // background: '#24292e', // Slightly lighter for elements considered "paper"

    // background: '#171717', // Slightly lighter for elements considered "paper"
    color: '#fff', // White text color
    // borderBottom: '2px solid #000', // Slightly darker border at the bottom

    borderBottom: '1px solid #424242', // Slightly darker border at the bottom
    fontFamily: 'Arial, sans-serif', // Font family for the title bar text
    title: {
      align: 'left', // Align the title text to the left
      color: 'inherit', // White title text color
    },
    button: {
      maxWidth: 120, // Maximum width for menu buttons
      default: { background: '#333', color: '#fff' }, // Default state colors
      hover: { background: '#444', color: '#fff' }, // Hover state colors
      active: { background: '#555', color: '#fff' }, // Active state colors
    },
  },
  controls: {
    layout: 'right', // Position the controls on the right
    normal: {
      // default: { background: '#171717', color: '#fff' },
      default: { background: '#212121', color: '#fff' },
      hover: { background: '#444', color: '#fff' },
    },
    close: {
      // default: { background: '#171717', color: '#fff' },
      default: { background: '#212121', color: '#fff' },
      hover: { background: '#444', color: '#fff' },
    },
  },
  menu: {
    palette: 'dark',
    style: 'default', // Use the default menu style
    item: {
      height: 20, // Height for menu items
      default: { background: '#333', color: '#fff' },
      active: { background: '#444', color: '#fff' },
    },
    separator: {
      color: '#444', // Color for separators in the menu
    },
  },

};


const win32Theme: TitleBarTheme = {
  platform: 'win32', // Specify the platform ('win32', 'linux', 'darwin')
  bar: {
    palette: 'dark', // Choose between 'light' or 'dark'
    height: '42px', // Set the bar height
    background: '#212121', // Slightly lighter for elements considered "paper"
    // background: '#24292e', // Slightly lighter for elements considered "paper"

    // background: '#171717', // Slightly lighter for elements considered "paper"
    color: '#fff', // White text color
    // borderBottom: '2px solid #000', // Slightly darker border at the bottom

    borderBottom: '1px solid #424242', // Slightly darker border at the bottom
    fontFamily: 'Arial, sans-serif', // Font family for the title bar text
    title: {
      align: 'left', // Align the title text to the left
      color: 'inherit', // White title text color
    },
    button: {
      maxWidth: 120, // Maximum width for menu buttons
      default: { background: '#333', color: '#fff' }, // Default state colors
      hover: { background: '#444', color: '#fff' }, // Hover state colors
      active: { background: '#555', color: '#fff' }, // Active state colors
    },
  },
  controls: {
    layout: 'right', // Position the controls on the right
    normal: {
      // default: { background: '#171717', color: '#fff' },
      default: { background: '#212121', color: '#fff' },
      hover: { background: '#444', color: '#fff' },
    },
    close: {
      // default: { background: '#171717', color: '#fff' },
      default: { background: '#212121', color: '#fff' },
      hover: { background: '#444', color: '#fff' },
    },
  },
  menu: {
    palette: 'dark',
    style: 'default', // Use the default menu style
    item: {
      height: 20, // Height for menu items
      default: { background: '#333', color: '#fff' },
      active: { background: '#444', color: '#fff' },
    },
    separator: {
      color: '#444', // Color for separators in the menu
    },
  },

};



function determineCurrentPlatform(): Platform {
  // This example assumes a Node.js or Electron environment; adjust as necessary.
  // For browser-based projects, you might not have access to process.platform
  // and may need a different strategy based on your environment.
  return process.platform as Platform;
}

// Determine the current platform
const currentPlatform = determineCurrentPlatform();

// Select the appropriate theme based on the platform
let customTheme: TitleBarTheme;
switch (currentPlatform) {
  case 'win32':
    customTheme = win32Theme;
    break;
  case 'linux':
    customTheme = linuxTheme;
    break;
  case 'darwin':
    customTheme = DarwinTheme;
    break;
  default:
    customTheme = win32Theme; // Default to Win32 theme if unsure
}


import { TitleBarTheme } from "frameless-titlebar/dist/title-bar/typings";
import { ipcRenderer } from 'electron';

export default function App(): JSX.Element {

  const handleClose = () => {
    // Send IPC message to close window
    ipcRenderer.send('close-window');
  };

  const handleMinimize = () => {
    ipcRenderer.send('minimize-window');
  }

  const handleMaximize = () => {
    ipcRenderer.send('maximize-window');
  }

  return (
    // Setup theme and css baseline for the Material-UI app
    // https://mui.com/customization/theming/
    //
    <ThemeProvider theme={theme}>
      <div style={{ position: 'fixed', width: '100%', zIndex: 1000 }}>
        <TitleBar
          theme={customTheme}
          onClose={handleClose}
          onMinimize={handleMinimize}
          onMaximize={handleMaximize}
        />
      </div>

      <CssBaseline />
      <BrowserRouter>
        <AuthProvider>
          <Box
            sx={{
              backgroundColor: (theme) => theme.palette.background.default,
            }}
          >
            {/*   <main>  */}
            {/* <Signin /> */}
            {/*   <Routes> */}
            {/*     <Route path="/" element={<Signin />} /> */}
            {/*     <Route path="/main" element={<Main />} /> */}
            {/*     <Route path="/register" element={<Signup />} /> */}
            {/*     <Route path="/login" element={<Signin />} /> */}
            {/*     <Route path="/settings" element={<Settings />} /> */}
            {/*     <Route path="/profile" element={<Profile />} /> */}
            {/*   </Routes> */}
            {/* </main> */}


            <main>
              <Signin />
              {/* <Routes> */}
              {/*   <Route path="/" element={<Signin />} /> */}
              {/*   <Route path="/login" element={<Signin />} /> */}
              {/*   <Route path="/register" element={<Signup />} /> */}
              {/* </Routes> */}
            </main>
            {/* <Main /> */}

          </Box>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

