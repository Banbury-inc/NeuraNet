import * as React from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import Divider from '@mui/material/Divider';
import Tooltip from '@mui/material/Tooltip';
import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import Login from './Login';
import isAuthenticated from './Login';
import setshowMain from './Login';
import { fontSize } from '@mui/system';
export default function AccountMenuIcon() {
  const { username, first_name, last_name, setFirstname, setLastname, redirect_to_login, setredirect_to_login } = useAuth();
  const [showLogin, setShowLogin] = useState<boolean>(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/${username}/`);
        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        setFirstname(fetchedFirstname);
        setLastname(fetchedLastname);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    setredirect_to_login(true);
    localStorage.removeItem('authToken');

  };

  const handleSettingsClick = () => {
    // Programmatically navigate to the main page and set the active tab
    navigate('/main', { state: { activeTab: 'Settings' } });
    handleClose(); // Close the menu after clicking on settings
  };


  return (
    <React.Fragment>
      <Box sx={{ mr: '20px', pb: '2px', display: 'flex', alignItems: 'center', textAlign: 'center' }}>
        <Tooltip title="Account">
          <Chip
            avatar={
              <Avatar sx={{}} variant="circular">
                {first_name?.charAt(0) || ''}
              </Avatar>
            }
            label={`${first_name || ''} ${last_name || ''}`}
            onClick={handleClick}
            size="small"
            aria-controls={open ? 'account-menu' : undefined}
            aria-haspopup="true"
            aria-expanded={open ? 'true' : undefined}
            sx={{ fontSize: '12px' }}
          />
        </Tooltip>
      </Box>
      <Menu
        anchorEl={anchorEl}
        id="account-menu"
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        PaperProps={{
          elevation: 0,
          sx: {
            fontSize: 'inherit',
            overflow: 'visible',
            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
            mt: 1.5,
            '& .MuiAvatar-root': {
              width: 22,
              height: 22,
              ml: -0.5,
              mr: 2,
            },
            '&::before': {
              content: '""',
              display: 'block',
              position: 'absolute',
              top: 0,
              right: 14,
              width: 10,
              height: 10,
              bgcolor: 'background.default',
              transform: 'translateY(-50%) rotate(45deg)',
              zIndex: 0,
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={handleClose}>
          <Avatar sx={{ width: 2, height: 2 }} /> Profile
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleClose}>
          <ListItemIcon>
            <PersonAddIcon fontSize="inherit" />
          </ListItemIcon>
          Add another account
        </MenuItem>
        <MenuItem onClick={handleSettingsClick}>
          <ListItemIcon>
            <SettingsIcon fontSize="inherit" />
          </ListItemIcon>
          Settings
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <LogoutIcon fontSize="inherit" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>
    </React.Fragment>
  );
}


