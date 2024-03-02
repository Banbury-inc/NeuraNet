import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";
import Login from "./components/Login";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement!);
// root.render(<App />);
root.render(<Login />);
