import { createTheme } from "@mui/material/styles";

// Create a Material-UI theme instance
// https://mui.com/customization/theming/
const theme = createTheme({
  palette: {
    mode: 'dark', // Spotify uses a dark theme
    background: {
      default: '#121212', // Very dark gray, almost black, as the main background
      paper: '#121212', // Slightly lighter for elements considered "paper"
    },
    primary: {
      main: '#90caf9', // Spotify's brand green for primary actions and highlights
      light: '#e3f2fd', // Spotify's brand green for primary actions and highlights
      dark: '#42a5f5', // Spotify's brand green for primary actions and highlights
    },
    secondary: {
      main: '#ce93d8', // A medium gray for secondary elements, might need adjustment
      light: '#f2e5f5', // A medium gray for secondary elements, might need adjustment
      dark: '#ab47bc', // A medium gray for secondary elements, might need adjustment
    },
    error: {
      main: '#f44336', // Just an example, adjust based on your preference
      light: '#e57373', // Just an example, adjust based on your preference
      dark: '#d32f2f', // Just an example, adjust based on your preference
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#B3B3B3', // Light gray for less important text, adjust as needed
    },
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
