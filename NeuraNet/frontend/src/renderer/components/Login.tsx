import * as React from 'react';
import { useState } from 'react';
import { exec } from "child_process";
import Avatar from '@mui/material/Avatar';
import NeuraNet_Logo from '/static/NeuraNet_Logo_White_No_Background.png';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import theme from "../theme";
import App from './App';
import { createRoot } from "react-dom/client";
import MiniDrawer from "./VariantDrawer";
import { BrowserRouter, Route, Routes, Outlet, Navigate } from "react-router-dom";
import Signup from "./signup";
import Main from "./main";
import { useAuth } from '../context/AuthContext';

function Copyright(props: any) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://website2-v3xlkt54dq-uc.a.run.app/">
        Banbury
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const path = require('path');
const cp = require("child_process");
const util = require("util");
const execFile = util.promisify(cp.execFile);

const fs = require("fs");


export default function SignIn() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const { setUsername } = useAuth();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const email = data.get('email') as string | null; // Cast the value to string
    const password = data.get('password') as string | null; // Cast the value to string
    console.log({
      email: data.get('email'),
      password: data.get('password'),
    });


    try {




  const { spawn } = require("child_process");
  const env = process.env.NODE_ENV || 'development';
  let baseDir = '';
  let devbaseDir = 'python';
  let prodbaseDir = path.join(process.resourcesPath, 'python');
  if (env === 'development') {
    baseDir = devbaseDir;
  } else if (env === 'production') {
    baseDir = prodbaseDir;
  }
  const scriptPath = path.join(baseDir, 'signin2.py');
  const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';


      // const scriptPath = 'src/main/signin2.py'; // Update this to the path of your Python script
  
      // const path_to_python = 'python3'; // Update this to the path of your Python script
      // const scriptPath = 'resources/python/signin2.py'; // Update this to the path of your Python script

      exec(`${pythonCommand} "${scriptPath}" "${data.get('email')}" "${data.get('password')}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return;
        }
        if (stdout && stdout.trim() === 'Result: success') {
          console.log('Login successful');
          console.log(email)
          setUsername(email); // Set username in context
          setIsAuthenticated(true);
        }
      });
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  if (isAuthenticated) {

    return <Main />;


  }

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* <Avatar sx={{ mt: 10, bgcolor: 'primary.main' }}> */}

            {/* <LockOutlinedIcon /> */}
          {/* </Avatar> */}
          {/* <img src={NeuraNet_Logo} alt="Logo" style={{ marginTop: 100, marginBottom: 20, width: 157.2, height: 137.2 }} /> */}
          <img src={NeuraNet_Logo} alt="Logo" style={{ marginTop: 100, marginBottom: 20, width: 78.6, height: 68.6 }} />
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Username"
              name="email"
              autoComplete="email"
              size='small'
              autoFocus
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              size='small'
              id="password"
              autoComplete="current-password"
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
 
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              // label="Remember me"
              label={<Typography style={{ fontSize: '15px' }}>Remember me</Typography>}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="/register" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="/register" variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
        <Copyright sx={{ mt: 5 }} />
      </Container>
    </ThemeProvider>
  );
}



