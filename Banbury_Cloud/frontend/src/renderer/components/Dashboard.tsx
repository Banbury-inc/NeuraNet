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
import AccountMenuIcon from "./AccountMenuIcon";
import { useAuth } from '../context/AuthContext';



export default function Dashboard(): JSX.Element {


  // Initialize state to store the first name
   useEffect(() => {
    // Function to fetch data
    const fetchData = async () => {
      try {
        // Make sure to use the correct endpoint that returns the expected data
        // const response = await axios.get('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');

        const { username } = useAuth();
        const response = await axios.get('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        //const response = await axios.get('http://localhost:8080/getuserinfo/');
        //const response = await axios.get('http://localhost:8080/users/');
        const data = response.data;
        // Set the fetched first name to state
        const last_total_device_storage = data.total_device_storage[data.total_device_storage.length-1];
        const last_number_of_devices = data.total_number_of_devices[data.total_number_of_devices.length-1];
        const last_number_of_files = data.total_number_of_files[data.total_number_of_files.length-1];
        const last_total_average_download_speed = data.total_average_download_speed[data.total_average_download_speed.length-1];
        const last_total_average_upload_speed = data.total_average_upload_speed[data.total_average_upload_speed.length-1];
        const number_of_devices = data.total_number_of_devices[data.total_number_of_devices-1];
        const total_average_download_speed = data.total_average_download_speed[data.total_average_download_speed-1];
        const total_average_upload_speed = data.total_average_upload_speed[data.total_average_upload_speed-1];
        const number_of_files = data.total_number_of_files[data.total_number_of_files-1];
        set_total_device_storage(last_total_device_storage.toFixed(2))
        set_number_of_devices(last_number_of_devices.toFixed(2))
        set_number_of_files(last_number_of_files.toFixed(2))
        set_total_average_download_speed(last_total_average_download_speed.toFixed(2))
        set_total_average_upload_speed(last_total_average_upload_speed.toFixed(2))


      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Call fetchData inside useEffect
    fetchData();
  }, []);

 
   const [total_device_storage, set_total_device_storage] = useState('');
  const [number_of_devices, set_number_of_devices] = useState('');
  const [number_of_files, set_number_of_files] = useState('');
  const [total_average_download_speed, set_total_average_download_speed] = useState('');
  const [total_average_upload_speed, set_total_average_upload_speed] = useState('');
  const [total_average_cpu_usage, set_total_average_cpu_usage] = useState('');
  const [Firstname, setFirstname] = useState<string>('');
  const [Lastname, setLastname] = useState<string>('');
  const { username } = useAuth();
  console.log(username)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[] 
          first_name: string;
          last_name: string;
          number_of_devices: any[]
          number_of_files: any[]
          total_average_download_speed: any[]
          total_average_upload_speed: any[]
          total_average_cpu_usage: any[]
          total_device_storage: any[]
        // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');

        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        const last_number_of_devices = response.data.number_of_devices[response.data.number_of_devices.length-1];
        const last_number_of_files = response.data.number_of_files[response.data.number_of_files.length-1];
        const last_total_average_download_speed = response.data.total_average_download_speed[response.data.total_average_download_speed.length-1];
        const last_total_average_upload_speed = response.data.total_average_upload_speed[response.data.total_average_upload_speed.length-1];
        const last_total_device_storage = response.data.total_device_storage[response.data.total_device_storage.length-1];
        set_number_of_devices(last_number_of_devices.toFixed(0))
        set_number_of_files(last_number_of_files.toFixed(0))
        set_total_average_download_speed(last_total_average_download_speed.toFixed(2))
        set_total_average_upload_speed(last_total_average_upload_speed.toFixed(2))
        set_total_device_storage(last_total_device_storage.toFixed(2))
        setFirstname(fetchedFirstname); 
        setLastname(fetchedLastname); 

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();

  },

  []);




return (
  <Container>

    <Grid container spacing={2}>
      <Box sx={{ maxwidth: '100%', p: 4, height: '100vh' }}>

        <Stack spacing={2}>
        <Stack direction = "row" justifyContent="space-between">
        <Grid item>
          <Typography variant="h2" textAlign="left">
            Dashboard
          </Typography>
          </Grid>
        <Grid item>
                <AccountMenuIcon />
          </Grid>
        </Stack> 
        </Stack> 

        <Stack spacing={2}>


    <Grid container sx={{pt:4}} spacing={2}>

                <Stack  spacing={2} direction="row" justifyContent="space-between">
          <Stack spacing={2}>
                <Stack  spacing={2} direction="row" justifyContent="space-between">
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
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
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="body2">
                    Devices Online
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {number_of_devices}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="body2">
                    Total Number of Files
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {number_of_files}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            </Stack>
          <Stack spacing={2}>
                <Stack  spacing={2} direction="row" justifyContent="space-between">
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="body2">
                    Average Upload Speed
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {total_average_upload_speed} mb/s
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="body2">
                    Average Download Speed
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {total_average_download_speed} mb/s
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card sx={{ width: '100%' }}>
                <CardContent>
                  <Typography variant="body2">
                    Total Device Storage
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {total_device_storage} GB
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            </Stack>
            </Stack>
 
          <Grid item style={{ maxHeight: '50vh' }}>
            <Card>
              <CardContent>
                <Typography variant="body2">
                  Total Number of Files
                  <br />
                </Typography>
                <Typography variant="h4" component="div">
                  {number_of_files}
                </Typography>
                {/* <TotalFilesChart /> */}
                <LineChart
                  xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
                  series={[
                    {
                      data: [200, 500, 550, 700, 600, 800],
                    },
                  ]}
                  width={550}
                  // height={375}
                />
 
              </CardContent>
            </Card>
          </Grid>
          </Stack>

 
          <Grid item style={{ minWidth: '400', maxHeight: '75vh' }}>
              <Card>
                <CardContent>
                  <Typography variant="body2">
                    Total Device Storage
                    <br />
                  </Typography>
                  <Typography variant="h4" component="div">
                    {total_device_storage} Gb
                  </Typography>
                  <PieActiveArc />
                </CardContent>
              </Card>
            </Grid>


       </Stack>
            </Grid>
       </Stack>

      </Box>
    </Grid>
  </Container>
);
}import { LineChart } from "@mui/x-charts";

