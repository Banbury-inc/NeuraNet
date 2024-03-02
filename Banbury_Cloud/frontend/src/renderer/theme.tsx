import { createTheme } from "@mui/material/styles";

// Create a Material-UI theme instance
// https://mui.com/customization/theming/
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      //main: "#7289da",
      main: "#FF6F00",
    },
    secondary: {
      //main: "#7289da",
      main: "#425066",
    },
  },
  typography: {
    fontWeightMedium: 400,
    fontSize: 16,
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    h1: {
      fontSize: "2.2rem",
      color: "#ffffff",
    },
    h2: {
      fontSize: "1.7rem",
      color: "#ffffff",
    },
    body1: {
      color: "#ffffff",
      fontSize: "1.7rem",
    },
  },

});

export default theme;
