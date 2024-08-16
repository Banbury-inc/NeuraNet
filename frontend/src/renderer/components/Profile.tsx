import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import DeleteIcon from '@mui/icons-material/Delete';
import FilterListIcon from '@mui/icons-material/FilterList';
import { Container, Typography, Grid, Button } from "@mui/material";
import Chip from '@mui/material/Chip';
import Avatar from '@mui/material/Avatar';
import { Stack } from '@mui/material';
import LineChart from './LineChart';
import { exec } from "child_process";
import AccountMenuIcon from './AccountMenuIcon';
import { useAuth } from '../context/AuthContext';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import { Email } from '@mui/icons-material';
import * as path from "path";
import * as change_profile_info from './scripts/change_profile_info'


interface Device {
  device_number: number;
  device_name: string;
  storage_capacity_GB: any;
  average_cpu_usage: number;
  average_download_speed: number;
  average_gpu_usage: number;
  average_ram_usage: number;
  average_time_online: number;
  average_upload_speed: number;
  onlineStatus: string;
  cpu_usage: number[];
  date_added: Date[];
  device_priority: number;
  download_network_speed: number[];
  gpu_usage: number[];
  ip_address: string;
  network_reliability: number;
  optimization_status: boolean;
  ram_usage: number[];
  sync_status: boolean;
  upload_network_speed: number[];
  online: boolean;
  // Add more device properties as needed
}

interface UserResponse {
  devices: Device[];
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  // Include other fields from your API response as needed
}


const { ipcRenderer } = window.require('electron');

ipcRenderer.on('python-output', (event: any, data: any) => {
  console.log('Received Python output:', data);
});




export default function Profile() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [selectedDeviceNames, setSelectedDeviceNames] = useState<string[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const { username } = useAuth();
  const [firstname, setFirstname] = useState<string>('');
  const [phone_number, setPhonenumber] = useState<string>('');
  const [lastname, setLastname] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const [deviceRows, setDeviceRows] = useState<Device[]>([]); // State for storing fetched file data
  const getSelectedDeviceNames = () => {
    return selected.map(device_number => {
      const device = deviceRows.find(device => device.device_number === device_number);
      return device ? device.device_name : null;
    }).filter(deviceName => deviceName !== null); // Filter out any null values if a file wasn't found
  };




  function formatBytes(gigabytes: number, decimals: number = 2): string {
    if (gigabytes === 0) return '0 GB';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    // Since we're starting from GB, there's no need to find the initial index based on the log.
    // Instead, we convert the input gigabytes to bytes to use the original formula,
    // adjusting it to start from GB.
    const bytes = gigabytes * Math.pow(k, 3); // Converting GB to Bytes for calculation
    const i = Math.floor(Math.log(bytes) / Math.log(k)) - 3; // Adjusting index to start from GB

    // Ensure the index does not fall below 0
    const adjustedIndex = Math.max(i, 0);
    return parseFloat((gigabytes / Math.pow(k, adjustedIndex)).toFixed(dm)) + ' ' + sizes[adjustedIndex];
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`https://website2-v3xlkt54dq-uc.a.run.app/get_small_user_info/${username}/`);
        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        const fetchedPhonenumber = response.data.phone_number;
        const fetchedemail = response.data.email;
        setFirstname(fetchedFirstname);
        setLastname(fetchedLastname);
        setPhonenumber(fetchedPhonenumber);
        setEmail(fetchedemail);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {

    const interval = setInterval(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get(`https://website2-v3xlkt54dq-uc.a.run.app/get_small_user_info/${username}/`);
          const fetchedFirstname = response.data.first_name;
          const fetchedLastname = response.data.last_name;

          // Processing data for the frontend, assuming your API returns data directly usable by the UI
          setFirstname(fetchedFirstname);
          setLastname(fetchedLastname);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };
      fetchData();
    }, 1000); // Refresh every 10 seconds 

    return () => clearInterval(interval);
  },
    []);


  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = devices.map((device) => device.device_number);
      setSelected(newSelected);
    } else {
      setSelected([]);
    }
  };

  const handleClick = (event: React.MouseEvent<unknown>, device_number: number) => {
    const selectedIndex = selected.indexOf(device_number);
    let newSelected: number[] = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, device_number);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1),
      );
    }
    setSelected(newSelected);

    const newSelectedDeviceNames = newSelected.map(device_number => deviceRows.find(device => device.device_number === device_number)?.device_name).filter(name => name !== undefined) as string[];
    setSelectedDeviceNames(newSelectedDeviceNames);
  };
  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };
  const isSelected = (device_number: number) => selected.indexOf(device_number) !== -1;



  const [showFirstnameTextField, setShowFirstnameTextField] = useState(false);
  const [new_first_name, set_new_first_name] = useState('');
  const handleFirstnameClick = async () => {
    try {
      setShowFirstnameTextField(!showFirstnameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };
  const handleFirstnameConfirmClick = async () => {

    setShowFirstnameTextField(!showFirstnameTextField);

    change_profile_info.change_profile_info(new_first_name, lastname, username, email, "undefined");
  };

  const [showLastnameTextField, setShowLastnameTextField] = useState(false);
  const [new_last_name, set_new_last_name] = useState('');
  const handleLastnameClick = async () => {
    try {
      setShowLastnameTextField(!showLastnameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };
  const handleLastnameConfirmClick = async () => {
    try {
      change_profile_info.change_profile_info(firstname, new_last_name, username, email, "undefined");
    } catch (error) {
      console.error('There was an error!', error);

    }
  };



  const [showUsernameTextField, setShowUsernameTextField] = useState(false);
  const [new_username, set_new_username] = useState('');
  const handleUsernameClick = async () => {
    try {
      setShowUsernameTextField(!showUsernameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };
  const handleUsernameConfirmClick = async () => {
    try {
      change_profile_info.change_profile_info(firstname, lastname, new_username, email, "undefined");
    } catch (error) {
      console.error('There was an error!', error);

    }
  };

  const [showEmailTextField, setShowEmailTextField] = useState(false);
  const [new_email, set_new_email] = useState('');
  const handleEmailClick = async () => {
    try {
      setShowEmailTextField(!showEmailTextField);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };
  const handleEmailConfirmClick = async () => {
    try {
      change_profile_info.change_profile_info(firstname, lastname, username, new_email, "undefined");
    } catch (error) {
      console.error('There was an error!', error);

    }
  };


  const [showPasswordTextField, setShowPasswordTextField] = useState(false);
  const [new_password, set_new_password] = useState('');
  const handlePasswordClick = async () => {
    try {
      setShowPasswordTextField(!showPasswordTextField);
    } catch (error) {
      console.error('There was an error!', error);
    }
  };
  const handlePasswordConfirmClick = async () => {
    try {
      change_profile_info.change_profile_info(firstname, lastname, username, email, new_password);
    } catch (error) {
      console.error('There was an error!', error);

    }
  };


  return (

    <Box sx={{ width: '100%', pl: 4, pr: 4, mt: 0, pt: 5 }}>
      <Stack spacing={2}>
        <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
          <Grid item>
            <Typography variant="h2" textAlign="left">
              Profile
            </Typography>
          </Grid>
          <Grid item>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
              <AccountMenuIcon />
            </Box>
          </Grid>
        </Grid>
        <Grid container spacing={1}>
        </Grid>
      </Stack>
      <Grid container spacing={2} columns={1}>
        <Grid item xs={8}>
          <Card variant='outlined'>
            <CardContent>
              <Box my={0}>
                <Stack spacing={4}>
                  <Typography variant="h4" gutterBottom>Account</Typography>
                  <Stack spacing={1}>
                    <Grid container justifyContent="space-between" alignItems="center" spacing={2}>

                      <Grid item>
                        <Typography variant="subtitle1" gutterBottom>First Name</Typography>
                        {showFirstnameTextField ? (
                          <TextField
                            id="Firstname"
                            size='small'
                            defaultValue={firstname}
                            onChange={(event) => set_new_first_name(event.target.value)}
                          />
                        ) : (
                          <Typography variant="body2" gutterBottom>{firstname}</Typography>
                        )}
                      </Grid>
                      {showFirstnameTextField ? (
                        <Grid item pr={4}>
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" onClick={handleFirstnameClick} size="small">
                              {showFirstnameTextField ? 'Cancel' : 'Change'}
                            </Button>
                            <Button variant="contained" color='success' onClick={handleFirstnameConfirmClick} size="small">
                              Submit
                            </Button>
                          </Stack>
                        </Grid>

                      ) : (
                        <Grid item pr={4}>
                          <Button variant="outlined" onClick={handleFirstnameClick} size="small">
                            {showFirstnameTextField ? 'Cancel' : 'Change'}
                          </Button>
                        </Grid>
                      )}
                    </Grid>
                    <Divider orientation="horizontal" variant="middle" />


                    <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
                      <Grid item>
                        <Typography variant="subtitle1" gutterBottom>Last Name</Typography>
                        {showLastnameTextField ? (
                          <TextField
                            id="Lastname"
                            size='small'
                            defaultValue={lastname}
                            onChange={(event) => set_new_last_name(event.target.value)}
                          />
                        ) : (
                          <Typography variant="body2" gutterBottom>{lastname}</Typography>
                        )}
                      </Grid>
                      {showLastnameTextField ? (
                        <Grid item pr={4}>
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" onClick={handleLastnameClick} size="small">
                              {showLastnameTextField ? 'Cancel' : 'Change'}
                            </Button>
                            <Button variant="contained" color='success' onClick={handleLastnameConfirmClick} size="small">
                              Submit
                            </Button>
                          </Stack>
                        </Grid>

                      ) : (
                        <Grid item pr={4}>
                          <Button variant="outlined" onClick={handleLastnameClick} size="small">
                            {showUsernameTextField ? 'Cancel' : 'Change'}
                          </Button>
                        </Grid>
                      )}
                    </Grid>
                    <Divider orientation="horizontal" variant="middle" />


                    <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
                      <Grid item>
                        <Typography variant="subtitle1" gutterBottom>Username</Typography>
                        {showUsernameTextField ? (
                          <TextField
                            id="Username"
                            size='small'
                            defaultValue={username}
                            onChange={(event) => set_new_username(event.target.value)}
                          />
                        ) : (
                          <Typography variant="body2" gutterBottom>{username}</Typography>
                        )}
                      </Grid>
                      {showUsernameTextField ? (
                        <Grid item pr={4}>
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" onClick={handleUsernameClick} size="small">
                              {showUsernameTextField ? 'Cancel' : 'Change'}
                            </Button>
                            <Button variant="contained" color='success' onClick={handleUsernameConfirmClick} size="small">
                              Submit
                            </Button>
                          </Stack>
                        </Grid>

                      ) : (
                        <Grid item pr={4}>
                          <Button variant="outlined" onClick={handleUsernameClick} size="small">
                            {showUsernameTextField ? 'Cancel' : 'Change'}
                          </Button>
                        </Grid>
                      )}
                    </Grid>
                    <Divider orientation="horizontal" variant="middle" />



                    <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
                      <Grid item>
                        <Typography variant="subtitle1" gutterBottom>Email</Typography>
                        {showEmailTextField ? (
                          <TextField
                            id="email"
                            size='small'
                            defaultValue={Email}
                            onChange={(event) => set_new_email(event.target.value)}
                          />
                        ) : (
                          <Typography variant="body2" gutterBottom>{email}</Typography>
                        )}
                      </Grid>
                      {showEmailTextField ? (
                        <Grid item pr={4}>
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" onClick={handleEmailClick} size="small">
                              {showEmailTextField ? 'Cancel' : 'Change'}
                            </Button>
                            <Button variant="contained" color='success' onClick={handleEmailConfirmClick} size="small">
                              Submit
                            </Button>
                          </Stack>
                        </Grid>

                      ) : (
                        <Grid item pr={4}>
                          <Button variant="outlined" onClick={handleEmailClick} size="small">
                            {showEmailTextField ? 'Cancel' : 'Change'}
                          </Button>
                        </Grid>
                      )}
                    </Grid>
                    <Divider orientation="horizontal" variant="middle" />


                    <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
                      <Grid item>
                        <Typography variant="subtitle1" gutterBottom>Password</Typography>
                        {showPasswordTextField ? (
                          <TextField
                            id="password"
                            size='small'
                            defaultValue=""
                            type="password"
                            onChange={(event) => set_new_password(event.target.value)}
                          />
                        ) : (
                          <Typography variant="body2" gutterBottom>Change your account password.</Typography>
                        )}
                      </Grid>
                      {showPasswordTextField ? (
                        <Grid item pr={4}>
                          <Stack direction="row" spacing={2}>
                            <Button variant="outlined" onClick={handlePasswordClick} size="small">
                              {showPasswordTextField ? 'Cancel' : 'Change'}
                            </Button>
                            <Button variant="contained" color='success' onClick={handlePasswordConfirmClick} size="small">
                              Submit
                            </Button>
                          </Stack>
                        </Grid>

                      ) : (
                        <Grid item pr={4}>
                          <Button variant="outlined" onClick={handlePasswordClick} size="small">
                            {showPasswordTextField ? 'Cancel' : 'Change'}
                          </Button>
                        </Grid>
                      )}
                    </Grid>
                    <Divider orientation="horizontal" variant="middle" />




                    <Stack spacing={1}>
                      <Grid container columns={12} justifyContent="space-between" alignItems="center" spacing={2}>
                        <Grid item>
                          <Typography variant="subtitle1" gutterBottom>Delete Account</Typography>
                          <Typography variant="body2" gutterBottom>Permanently delete your account, licenses, and subscriptions.
                            You will be asked for confirmation before deletion proceeds.</Typography>
                        </Grid>
                        <Grid item pr={4}>
                          <Button variant="outlined" color="error" onClick={handleFirstnameClick} size="small">
                            Delete
                          </Button>
                        </Grid>
                      </Grid>

                    </Stack>
                  </Stack>
                </Stack>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>

  );
}

