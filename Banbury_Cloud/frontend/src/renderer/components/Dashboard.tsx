import { Box, Container, Grid, Typography } from "@mui/material";

import React, { useEffect, useState } from 'react';
import electronLogo from "../../../static/electron.svg";
import DifferentLength from "./LineChart";
import PieActiveArc from "./Piechart";
import BasicCard from "./card";
import Average_Wifi_Speed from "./average_wifi_speed";
import TotalNumberofFiles from "./total_number_of_files";
import TotalNumberofDevices from "./total_number_of_devices";
import Stack from '@mui/material/Stack';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import axios from 'axios';
import TotalFilesChart from "./TotalFilesChart";
import AverageWifiChart from "./AverageWifiChart";


export default function Dashboard(): JSX.Element {


  // Initialize state to store the first name
  const [total_device_storage, set_total_device_storage] = useState('');
  const [number_of_devices, set_number_of_devices] = useState('');
  const [number_of_files, set_number_of_files] = useState('');
  const [total_average_download_speed, set_total_average_download_speed] = useState('');

  useEffect(() => {
    // Function to fetch data
    const fetchData = async () => {
      try {
        // Make sure to use the correct endpoint that returns the expected data
        const response = await axios.get('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');
        //const response = await axios.get('http://localhost:8080/getuserinfo/');
        //const response = await axios.get('http://localhost:8080/users/');
        const data = response.data;
        // Set the fetched first name to state
        const last_total_device_storage = data.total_device_storage[data.total_device_storage.length-1];
        const last_number_of_devices = data.total_number_of_devices[data.total_number_of_devices.length-1];
        const last_number_of_files = data.total_number_of_files[data.total_number_of_files.length-1];
        const last_total_average_download_speed = data.total_average_download_speed[data.total_average_download_speed.length-1];
        const number_of_devices = data.total_number_of_devices[data.total_number_of_devices-1];
        const total_average_download_speed = data.total_average_download_speed[data.total_average_download_speed-1];
        const number_of_files = data.total_number_of_files[data.total_number_of_files-1];
        set_total_device_storage(last_total_device_storage.toFixed(2))
        set_number_of_devices(last_number_of_devices.toFixed(2))
        set_number_of_files(last_number_of_files.toFixed(2))
        set_total_average_download_speed(last_total_average_download_speed.toFixed(2))




      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Call fetchData inside useEffect
    fetchData();
  }, []);

 


  return (
    <Container>
      <Grid container spacing={2}>
      <Box sx={{ width: '100%', pt: 4 }}>
    <Stack spacing={2}>
      <Typography variant="h2" textAlign="left">
        Dashboard
      </Typography>
  <Stack direction="row" spacing={2}>
       <Grid item xs={3}>
     <Card>
      <CardContent>
       <Typography variant="body2">
          Total Number of Devices
          <br />
        </Typography>
       <Typography variant="h4" component="div">
          {number_of_devices}
        </Typography>
     </CardContent>
   </Card>
         </Grid>

       <Grid item xs={3}>
<Card>
 <CardContent>
  <Typography variant="body2">
     Total Number of Devices
     <br />
   </Typography>
  <Typography variant="h4" component="div">
     {number_of_devices}
   </Typography>
</CardContent>
</Card>
    </Grid>

       <Grid item xs={3}>
     <Card>
      <CardContent>
       <Typography variant="body2">
          Total Number of Devices
          <br />
        </Typography>
       <Typography variant="h4" component="div">
          {number_of_devices}
        </Typography>
     </CardContent>
   </Card>
         </Grid>
 

        <Grid item>
    <Card sx={{ minWidth: 400 }}>
      <CardContent>
        <Typography variant="body2">
          Total Device Storage
          <br />
        </Typography>
        <Typography variant="h4" component="div">
          {/* Display the fetched first name */}
          {total_device_storage} Gb
        </Typography>
        <PieActiveArc />
      </CardContent>
    </Card>
 
         </Grid>

 </Stack>
        <Grid item>
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
       <Typography variant="body2">
          Total Number of Files
          <br />
        </Typography>
       <Typography variant="h4" component="div">
          {number_of_files}
        </Typography>
        <TotalFilesChart />
     </CardContent>
   </Card>
 
         </Grid>

     </Stack>
     </Box>

         </Grid>
    </Container>
  );
}
