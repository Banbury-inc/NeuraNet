import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import { useState } from 'react';
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
import { exec } from "child_process";
import SignIn from './Login';

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

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function SignUp() {
  const [registration_success, setregistration_success] = useState(false);


  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
   event.preventDefault();
  const data = new FormData(event.currentTarget);
  const email = data.get('email') as string | null; // Cast the value to string
  const password = data.get('password') as string | null; // Cast the value to string
  const firstName = data.get('firstName') as string | null; // Cast the value to string
  const lastName = data.get('lastName') as string | null; // Cast the value to string
 
    console.log({
      firstName: data.get('firstName'),
      lastName: data.get('lastName'),
      username: data.get('username'),
      password: data.get('password'),
    });


    try {
      const scriptPath = 'src/main/signup.py'; // Update this to the path of your Python script
      exec(`python "${scriptPath}" "${data.get('username')}" "${data.get('password')}" "${data.get('firstName')}" "${data.get('lasttName')}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          console.log(error)
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          console.log(stderr)
          return;
        }
        if (stdout && stdout.trim() === 'Result: success') {
          console.log('registration successful');
          console.log(email)
          console.log(stdout)
          setregistration_success(true);
        }
      });
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  if (registration_success) {

    return <SignIn />;



  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="firstName"
                  required
                  fullWidth
                  id="firstName"
                  label="First Name"
                  size='small'
                  autoFocus
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
 
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="lastName"
                  label="Last Name"
                  name="lastName"
                  size='small'
                  autoComplete="family-name"
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
 
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  size='small'
                  autoComplete="username"
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
 
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  size='small'
                  id="password"
                  autoComplete="new-password"
              InputProps={{
                style: { fontSize: '1.7rem' }, // Adjusts text font size inside the input box
              }}
              InputLabelProps={{
                style: { fontSize: '1.3rem' }, // Adjusts the label font size
              }}
 
                />
              </Grid>

            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign Up
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/login" variant="body2">
                  Already have an account? Sign in
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
