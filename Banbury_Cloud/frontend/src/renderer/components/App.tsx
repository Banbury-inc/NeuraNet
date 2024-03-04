import { Box, CssBaseline, ThemeProvider } from "@mui/material";
import React from "react";
import theme from "../theme";
import PermanentDrawerLeft from "./Drawer";
import MiniDrawer from "./VariantDrawer";
import { BrowserRouter, Route, Routes, Outlet, Navigate } from "react-router-dom";
import Signup from "./signup";
import Signin from "./Login";
import Main from "./main";




export default function App(): JSX.Element {
  return (
    // Setup theme and css baseline for the Material-UI app
    // https://mui.com/customization/theming/
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter> {/* Wrap your content with BrowserRouter */}
        <Box
          sx={{
            backgroundColor: (theme) => theme.palette.background.default,
          }}
        >
          {/* <main> */}
            {/* This is where your app content should go */}
            {/* <MiniDrawer /> */}
          {/* </main> */}





          <Routes>
          
            {/* <Route path="/" element={<Signin />} /> */}
            <Route path="/" element={<Main />} />
            <Route path="/main" element={<MiniDrawer />} />
            <Route path="/register" element={<Signup />} />
            <Route path="/login" element={<Signin />} />
          </Routes>  



        </Box>
      </BrowserRouter>
    </ThemeProvider>
  );
}

