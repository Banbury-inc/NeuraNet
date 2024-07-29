import React, { useEffect } from 'react';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import { styled, useTheme, Theme, CSSObject } from '@mui/material/styles';
import MuiAppBar, { AppBarProps as MuiAppBarProps } from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MuiDrawer from '@mui/material/Drawer';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import Icon from '@mui/material/Icon';
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import SpaceDashboardOutlinedIcon from '@mui/icons-material/SpaceDashboardOutlined';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import AI from './AI';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import Files from './files';
import FolderOutlinedIcon from '@mui/icons-material/FolderOutlined';
import DevicesIcon from '@mui/icons-material/Devices';
import SettingsIcon from '@mui/icons-material/Settings';
import DashboardIcon from '@mui/icons-material/Dashboard';
import FolderIcon from '@mui/icons-material/Folder';
import EnhancedTable from "./Table";
import Dashboard from './Dashboard';
import Devices from "./Devices";
import DifferentLength from "./LineChart";
import { Stack, Chip, Grid } from '@mui/material';
import axios from 'axios';
import DevicesTable from './DeviceTable';
import Settings from './Settings';
import { useAuth } from '../context/AuthContext';
import { useLocation } from 'react-router-dom';
import AccountMenuIcon from './AccountMenuIcon';
import Login from './Login';
import Profile from './Profile';
import Tooltip from '@mui/material/Tooltip';
import net from 'net';
import * as receiver5 from '../../main/receiver5';
import { receiver, send_login_request, connectToRelayServer } from './scripts/receiver';

const { ipcRenderer } = window.require('electron');

const drawerWidth = 240;  // Change the width as needed
// const drawerWidth = 150;  // Change the width as needed

const openedMixin = (theme: Theme): CSSObject => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme: Theme): CSSObject => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(4)} + 8px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(4)} + 8px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(1, 1),
  ...theme.mixins.toolbar,
}));

interface AppBarProps extends MuiAppBarProps {
  open?: boolean;
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})<AppBarProps>(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

export default function PermanentDrawerLeft() {
  const location = useLocation();
  const theme = useTheme();
  const initialActiveTab = location.state?.activeTab || 'Files';
  const [activeTab, setActiveTab] = React.useState(initialActiveTab);
  const { username, redirect_to_login } = useAuth();
  const [open, setOpen] = React.useState(false);

  useEffect(() => {
    async function setupConnection() {
      try {
        console.log("connecting to relay server");
        let senderSocket = connectToRelayServer();
        console.log("Starting receiver");
        receiver(username, senderSocket);
        console.log("receiver has been started");
      } catch (error) {
        console.error("Failed to setup connection:", error);
      }
    }

    setupConnection();
  }, [username]);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const toggleDrawer = () => {
    setOpen(!open);
  };

  if (redirect_to_login) {
    return <Login />;
  }

  return (
    // <Box sx={{ display: 'flex', width: '100vw' }}>
    <Box sx={{ display: 'flex', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <CssBaseline />
      <Drawer
        sx={{
          '& .MuiDrawer-paper': {
            marginTop: '42px',
            paddingLeft: '2px',
            backgroundColor: theme.palette.background.default,
          },
        }}
        variant="permanent"
        open={open}
        anchor="left"
      >
        {/* <DrawerHeader> */}
        {/*   <IconButton */}
        {/*     color="inherit" */}
        {/*     aria-label="open drawer" */}
        {/*     onClick={toggleDrawer} */}
        {/*     edge="start" */}
        {/*     sx={{ */}
        {/*       marginRight: 0, */}
        {/*     }} */}
        {/*   > */}
        {/*     <MenuIcon /> */}
        {/*   </IconButton> */}
        {/* </DrawerHeader> */}

        <List>
          {['Files', 'Devices', 'Profile'].map((text, index) => (
            <Tooltip title={text} key={text} placement="right">
              <ListItem key={text} sx={{ padding: '2px', paddingTop: '2px' }}>
                <Button
                  onClick={() => setActiveTab(text)}
                  sx={{
                    paddingLeft: '4px',
                    paddingRight: '4px',
                    minWidth: '30px',
                  }} // Adjust the left and right padding as needed

                >
                  <Icon
                    fontSize="inherit"
                  >

                    {(() => {
                      switch (index % 5) {
                        // case 0:
                        // return <SpaceDashboardOutlinedIcon fontSize='inherit' />;
                        case 0:
                          return <FolderOutlinedIcon fontSize='inherit' />;
                        case 1:
                          return <DevicesIcon fontSize='inherit' />;
                        // case 3:
                        // return <AutoAwesomeIcon fontSize='inherit' />;
                        case 2:
                          return <AccountBoxIcon fontSize='inherit' />;
                        default:
                          return null;
                      }
                    })()}
                  </Icon>
                  {/*   <ListItemText */}
                  {/*     secondary={text} */}
                  {/*     sx={{ */}
                  {/*       opacity: open ? 1 : 1, */}
                  {/*       display: 'block', */}
                  {/*       textAlign: 'center', */}
                  {/*     }} */}
                  {/*   /> */}
                </Button>
              </ListItem>
            </Tooltip>
          ))}
        </List>
        <Divider />
        <List>
          {['Settings'].map((text) => (

            <Tooltip title={text} key={text} placement="right">
              <ListItem key={text} sx={{ padding: '2px' }}>
                <Button
                  sx={{
                    paddingLeft: '4px',
                    paddingRight: '4px',
                    minWidth: '30px',
                  }} // Adjust the left and right padding as needed

                  onClick={() => setActiveTab(text)}
                >
                  <Icon
                    fontSize='inherit'
                  >
                    <SettingsIcon fontSize='inherit' />
                  </Icon>
                  {/* <ListItemText */}
                  {/*   secondary={text} */}
                  {/*   sx={{ */}
                  {/*     opacity: open ? 1 : 1, */}
                  {/*     display: 'block', */}
                  {/*     textAlign: 'center', */}
                  {/*   }} */}
                  {/* /> */}
                </Button>
              </ListItem>
            </Tooltip>
          ))}
        </List>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: 'background.default', p: 0, width: 'calc(100vw - 240px)' }}
      >
        {(() => {
          switch (activeTab) {
            case 'Dashboard':
              return <Dashboard />;
            case 'Files':
              return <Files />;
            case 'Devices':
              return <DevicesTable />;
            case 'AI':
              return <AI />;
            case 'Profile':
              return <Profile />;
            case 'Settings':
              return <Settings />;
            default:
              return <Typography paragraph>Select a tab to display its content.</Typography>;
          }
        })()}
      </Box>
    </Box >
  );
}

