import { createTheme } from "@mui/material/styles";

// Create a Material-UI theme instance
// https://mui.com/customization/theming/
const theme = createTheme({
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          // borderWidth: '0.2px', // Set the desired border width
          borderRadius: 1, // Set the desired border radius
          borderColor: 'primary.main', // Set the desired border color
          // borderStyle: 'solid',
        },
      },
    },
  },

  palette: {
    mode: 'dark', // Spotify uses a dark theme
    background: {
      default: '#212121', // Slightly lighter for elements considered "paper"
      paper: '#171717', // Very dark gray, almost black, as the main background
    },
    primary: {
      main: '#FFFFFF', // Updated to match Material UI's primary blue color
      light: '#FFFFFF', // Updated to match Material UI's primary blue color
      dark: '#FFFFFF', // Updated to match Material UI's primary blue color
    },
    secondary: {
      main: '#000000', // Updated to match Material UI's secondary pink color
      light: '#000000', // Updated to match Material UI's secondary pink color
      dark: '#000000', // Updated to match Material UI's secondary pink color
    },
    error: {
      main: '#f44336', // Material UI's default error color
      light: '#e57373', // Material UI's default error color
      dark: '#d32f2f', // Material UI's default error color
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#B3B3B3', //ray for less important text, adjust as needed
    },
    divider: '#424242',

  },

  typography: {
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 600,
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
      fontWeight: 600,
      fontSize: '2.375rem',
      lineHeight: 1.21
    },
    h2: {
      fontWeight: 600,
      fontSize: '1.875rem',
      lineHeight: 1.27
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.33
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.4
    },
    h5: {
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: 1.5
    },
    h6: {
      fontWeight: 400,
      fontSize: '0.875rem',
      lineHeight: 1.57
    },
    caption: {
      fontWeight: 400,
      fontSize: '0.75rem',
      lineHeight: 1.66
    },
    body1: {
      fontSize: '0.875rem',
      lineHeight: 1.57
    },
    body2: {
      fontSize: '0.75rem',
      lineHeight: 1.66
    },
    subtitle1: {
      fontSize: '0.875rem',
      fontWeight: 600,
      lineHeight: 1.57
    },
    subtitle2: {
      fontSize: '0.75rem',
      fontWeight: 500,
      lineHeight: 1.66
    },
    overline: {
      lineHeight: 1.66
    },
    button: {
      textTransform: 'capitalize'
    }

  },

});


export default theme;
