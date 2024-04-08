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
  const [deviceRows, setDeviceRows] = useState<Device[]>([]); // State for storing fetched file data
  const getSelectedDeviceNames = () => {
    return selected.map(device_number => {
      const device = deviceRows.find(device => device.device_number === device_number);
      return device ? device.device_name : null;
    }).filter(deviceName => deviceName !== null); // Filter out any null values if a file wasn't found
  };


const handleApiCall = async () => {
  const selectedDeviceNames = getSelectedDeviceNames();
  }
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<UserResponse>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');

        const data = response.data;
        // Processing data for the frontend, assuming your API returns data directly usable by the UI
        const roundedDevices = data.devices.map(device => ({
          ...device,
          average_upload_speed: parseFloat(device.average_upload_speed.toFixed(2)),
          storage_capacity_GB: formatBytes(device.storage_capacity_GB),
          average_download_speed: parseFloat(device.average_download_speed.toFixed(2)),
          average_gpu_usage: parseFloat(device.average_gpu_usage.toFixed(2)),
          average_cpu_usage: parseFloat(device.average_cpu_usage.toFixed(2)),
          average_ram_usage: parseFloat(device.average_ram_usage.toFixed(2)),
          date_added: device.date_added.map(dateStr => new Date(dateStr)), // Transforming date strings to Date objects
          onlineStatus: device.online ? "Online" : "Offline"
        }));

        setDevices(roundedDevices);
        setDeviceRows(roundedDevices);
        setFirstname(data.first_name);
        setEmail(data.email);
        setLastname(data.last_name);
        setPassword(data.password);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);



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
    const interval = setInterval(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<UserResponse>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        const data = response.data;
        // Processing data for the frontend, assuming your API returns data directly usable by the UI
        const roundedDevices = data.devices.map(device => ({
          ...device,
          average_upload_speed: parseFloat(device.average_upload_speed.toFixed(2)),
          storage_capacity_GB: formatBytes(device.storage_capacity_GB),
          average_download_speed: parseFloat(device.average_download_speed.toFixed(2)),
          average_gpu_usage: parseFloat(device.average_gpu_usage.toFixed(2)),
          average_cpu_usage: parseFloat(device.average_cpu_usage.toFixed(2)),
          average_ram_usage: parseFloat(device.average_ram_usage.toFixed(2)),
          date_added: device.date_added.map(dateStr => new Date(dateStr)), // Transforming date strings to Date objects
          onlineStatus: device.online ? "Online" : "Offline"
        }));

        setDevices(roundedDevices);
        setDeviceRows(roundedDevices);
        setFirstname(data.first_name);
        setEmail(data.email);
        setLastname(data.last_name);
        setPassword(data.password);
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
  const [firstName, setFirstName] = useState('');
  const handleFirstnameClick = async () => {
    try{
      setShowFirstnameTextField(!showFirstnameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    } 
  };
  const handleFirstnameConfirmClick = async () => {
    try{

      setShowFirstnameTextField(!showFirstnameTextField);

      // const scriptPath = 'src/main/change_profile_info.py'; // Update this to the path of your Python script
       
       const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let devbaseDir = '';
      let filename = '';
      let command = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/change_profile_info.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'prod-receiver5.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';
      }

      const scriptPath = path.join(baseDir, filename);
      const commandPath = path.join(baseDir, command);
 


      exec(`${commandPath} "${scriptPath}" "${firstName}" "${Lastname}" "${username}" "${Email}" "${Password}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);
      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };

  const [showLastnameTextField, setShowLastnameTextField] = useState(false);
  const [lastName, setLastName] = useState('');
  const handleLastnameClick = async () => {
    try{
      setShowLastnameTextField(!showLastnameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    } 
  };
  const handleLastnameConfirmClick = async () => {
    try{

      setShowLastnameTextField(!showLastnameTextField);
       const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let devbaseDir = '';
      let filename = '';
      let command = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/change_profile_info.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'prod-receiver5.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';
      }

      const scriptPath = path.join(baseDir, filename);
      const commandPath = path.join(baseDir, command);
 


      // const scriptPath = 'src/main/change_profile_info.py'; // Update this to the path of your Python script
       
      exec(`${commandPath} "${scriptPath}" "${Firstname}" "${lastName}" "${username}" "${Email}" "${Password}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);
      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };



  const [showUsernameTextField, setShowUsernameTextField] = useState(false);
  const [new_username, setusername] = useState('');
  const handleUsernameClick = async () => {
    try{
      setShowUsernameTextField(!showUsernameTextField);
    } catch (error) {
      console.error('There was an error!', error);
    } 
  };
  const handleUsernameConfirmClick = async () => {
    try{

      setShowUsernameTextField(!showUsernameTextField);

      // const scriptPath = 'src/main/change_profile_info.py'; // Update this to the path of your Python script
       const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let devbaseDir = '';
      let filename = '';
      let command = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/change_profile_info.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'prod-receiver5.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';
      }

      const scriptPath = path.join(baseDir, filename);
      const commandPath = path.join(baseDir, command);
       
      exec(`${commandPath} "${scriptPath}" "${Firstname}" "${Lastname}" "${new_username}" "${Email}" "${Password}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);
      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };


  const [showEmailTextField, setShowEmailTextField] = useState(false);
  const [email, setemail] = useState('');
  const handleEmailClick = async () => {
    try{
      setShowEmailTextField(!showEmailTextField);
    } catch (error) {
      console.error('There was an error!', error);
    } 
  };
  const handleEmailConfirmClick = async () => {
    try{

      setShowEmailTextField(!showEmailTextField);

      // const scriptPath = 'src/main/change_profile_info.py'; // Update this to the path of your Python script
       const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let devbaseDir = '';
      let filename = '';
      let command = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/change_profile_info.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'prod-receiver5.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';
      }

      const scriptPath = path.join(baseDir, filename);
      const commandPath = path.join(baseDir, command);
      
      exec(`${commandPath} "${scriptPath}" "${Firstname}" "${Lastname}" "${username}" "${email}" "${Password}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);
      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };


  const [showPasswordTextField, setShowPasswordTextField] = useState(false);
  const [password, setpassword] = useState('');
  const handlePasswordClick = async () => {
    try{
      setShowPasswordTextField(!showPasswordTextField);
    } catch (error) {
      console.error('There was an error!', error);
    } 
  };
  const handlePasswordConfirmClick = async () => {
    try{

      setShowPasswordTextField(!showPasswordTextField);

       const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let devbaseDir = '';
      let filename = '';
      let command = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/change_profile_info.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'prod-receiver5.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';
      }

      const scriptPath = path.join(baseDir, filename);
      const commandPath = path.join(baseDir, command);
 
      exec(`${commandPath} "${scriptPath}" "${Firstname}" "${Lastname}" "${username}" "${Email}" "${password}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);
      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };




  const [Firstname, setFirstname] = useState<string>('');
  const [Lastname, setLastname] = useState<string>('');
  const [Email, setEmail] = useState<string>('');
  const [Password, setPassword] = useState<string>('');
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[] 
          first_name: string;
          last_name: string;
          email: string;
          password: string;
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username +'/');

        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        const fetchedEmail = response.data.email;
        const fetchedPassword = response.data.password;
        setEmail(fetchedEmail); 
        setFirstname(fetchedFirstname); 
        setLastname(fetchedLastname); 
        setPassword(fetchedPassword); 
        console.log(fetchedFirstname);
     } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);


  return (
    <Container>
      <Box sx={{ width: '100%', mt: 0, pt: 5 }}>
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
       {showFirstnameTextField ?  (
          <TextField
            id="Firstname"
            size='small'
            defaultValue={Firstname}
            onChange={(event) => setFirstName(event.target.value)}
          />
        ) : (
          <Typography variant="body2" gutterBottom>{Firstname}</Typography>
        )}
            </Grid>
       {showFirstnameTextField ?  (
            <Grid item pr={4}>
              <Stack direction="row" spacing={2}>
              <Button variant="outlined" onClick={handleFirstnameClick} size="small">
                {showFirstnameTextField ? 'Cancel' : 'Change'}
              </Button>
              <Button variant="contained" color='success'onClick={handleFirstnameConfirmClick} size="small">
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
       {showLastnameTextField ?  (
          <TextField
            id="Lastname"
            size='small'
            defaultValue={Lastname}
            onChange={(event) => setLastName(event.target.value)}
          />
        ) : (
          <Typography variant="body2" gutterBottom>{Lastname}</Typography>
        )}
            </Grid>
       {showLastnameTextField ?  (
            <Grid item pr={4}>
              <Stack direction="row" spacing={2}>
              <Button variant="outlined" onClick={handleLastnameClick} size="small">
                {showLastnameTextField ? 'Cancel' : 'Change'}
              </Button>
              <Button variant="contained" color='success'onClick={handleLastnameConfirmClick} size="small">
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
       {showUsernameTextField ?  (
          <TextField
            id="Username"
            size='small'
            defaultValue={username}
            onChange={(event) => setusername(event.target.value)}
          />
        ) : (
          <Typography variant="body2" gutterBottom>{username}</Typography>
        )}
            </Grid>
       {showUsernameTextField ?  (
            <Grid item pr={4}>
              <Stack direction="row" spacing={2}>
              <Button variant="outlined" onClick={handleUsernameClick} size="small">
                {showUsernameTextField ? 'Cancel' : 'Change'}
              </Button>
              <Button variant="contained" color='success'onClick={handleUsernameConfirmClick} size="small">
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
       {showEmailTextField ?  (
          <TextField
            id="email"
            size='small'
            defaultValue={Email}
            onChange={(event) => setemail(event.target.value)}
          />
        ) : (
          <Typography variant="body2" gutterBottom>{Email}</Typography>
        )}
            </Grid>
       {showEmailTextField ?  (
            <Grid item pr={4}>
              <Stack direction="row" spacing={2}>
              <Button variant="outlined" onClick={handleEmailClick} size="small">
                {showEmailTextField ? 'Cancel' : 'Change'}
              </Button>
              <Button variant="contained" color='success'onClick={handleEmailConfirmClick} size="small">
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
       {showPasswordTextField ?  (
          <TextField
            id="password"
            size='small'
            defaultValue=""
            type="password"
            onChange={(event) => setpassword(event.target.value)}
          />
        ) : (
          <Typography variant="body2" gutterBottom>Change your account password.</Typography>
        )}
            </Grid>
       {showPasswordTextField ?  (
            <Grid item pr={4}>
              <Stack direction="row" spacing={2}>
              <Button variant="outlined" onClick={handlePasswordClick} size="small">
                {showPasswordTextField ? 'Cancel' : 'Change'}
              </Button>
              <Button variant="contained" color='success'onClick={handlePasswordConfirmClick} size="small">
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

    </Container>
  );
}

