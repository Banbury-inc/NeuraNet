import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import Login from "./components/Login";
import axios from 'axios';
import * as fs from 'fs/promises';
import * as path from 'path';
import App from './components/App';
import MiniDrawer from "./components/VariantDrawer";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement!);
root.render(<App />);
