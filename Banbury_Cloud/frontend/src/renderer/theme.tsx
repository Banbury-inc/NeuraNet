import { createTheme } from "@mui/material/styles";

// Create a Material-UI theme instance
// https://mui.com/customization/theming/
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: "#7289da",
    },
    secondary: {
      main: "#7289da",
    },
  },
  typography: {
    fontWeightMedium: 600,
    fontSize: 17,
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
    body1: {
      color: "#ffffff",
    },
  },
});

export default theme;
