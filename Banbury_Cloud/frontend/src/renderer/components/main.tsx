import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import Files from './files';
import DevicesIcon from '@mui/icons-material/Devices';
import SettingsIcon from '@mui/icons-material/Settings';
import DashboardIcon from '@mui/icons-material/Dashboard';
import FolderIcon from '@mui/icons-material/Folder';
import EnhancedTable from "./Table" 
import Dashboard from './Dashboard';
import Devices from "./Devices" 
import DifferentLength from "./LineChart" 
import { Stack } from '@mui/material';
const drawerWidth = 240;
import { Chip } from '@mui/material';
import Grid from '@mui/material/Grid';
import DevicesTable from './DeviceTable';



export default function PermanentDrawerLeft() {


  const [activeTab, setActiveTab] = React.useState('Files');
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
      >
      {/*   <Toolbar> */}
      {/*     <Typography variant="h6" noWrap component="div"> */}
      {/*       Permanent drawer */}
      {/*     </Typography> */}
      {/*   </Toolbar> */}
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent"
        anchor="left"
      >
<Box
  sx={{
    display: 'flex',
    flexDirection: 'column', // Stack children vertically
    justifyContent: 'center', // Center children vertically in the container
    alignItems: 'center', // Center children horizontally in the container
    height: '7vh', // Take full height of the viewport
  }}
>

        <Stack direction="row" spacing={1} justifyContent="center">
          <Typography 
          variant="h3"
            >
            Banbury Cloud
          </Typography>
        </Stack>
</Box>
        <Divider />

        <List>
 
          {['Dashboard', 'Files', 'Devices'].map((text, index) => (
            <ListItem key={text} disablePadding>
                <ListItemButton onClick={() => setActiveTab(text)}>
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: 3,
                  justifyContent: 'center',
                }}
              >
                {(() => {
                  switch (index % 3) {
                    case 0:
                      return <DashboardIcon fontSize='inherit' />;
                    case 1:
                      return <FolderIcon fontSize='inherit'/>;
                    case 2:
                      return <DevicesIcon fontSize='inherit'/>;
                    default:
                      return null; // Just in case
                  }
                })()}
              </ListItemIcon>
                <ListItemText primary={text}
                />
              </ListItemButton>
            </ListItem>

          ))}

        </List>
        <Divider />
        <List>
          {['Settings'].map((text, index) => (
            <ListItem key={text} disablePadding>
              <ListItemButton>
                <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: 3,
                  justifyContent: 'center',
                }}
 
                >

                  {index % 2 === 0 ? <SettingsIcon fontSize='inherit'/> : <SettingsIcon fontSize='inherit'/>}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}

        </List>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: 'background.default', p: 0}}
      >
  {(() => {
    switch (activeTab) {
      case 'Dashboard':
        return <Dashboard />;
      case 'Files':
        return <Files />;
      case 'Devices':
        return <DevicesTable />;
      case 'Settings':
        // Replace <Typography> with your settings component
        return <Typography paragraph>Settings Component Here</Typography>;
      default:
        return <Typography paragraph>Select a tab to display its content.</Typography>;
    }
  })()}      
      </Box>


    </Box>
  );
}


