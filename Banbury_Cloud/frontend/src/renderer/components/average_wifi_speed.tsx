
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import AverageWifiChart from './AverageWifiChart';
const bull = (
  <Box
    component="span"
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

export default function Average_Wifi_Speed() {

  // Initialize state to store the first name
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
        //
      const lastAverageDownloadSpeed = data.total_average_download_speed[data.total_average_download_speed.length - 1];
      set_total_average_download_speed(lastAverageDownloadSpeed.toFixed(2));

        //set_total_average_download_speed(data.total_average_download_speed[data.total_average_download_speed.length - 1]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Call fetchData inside useEffect
    fetchData();
  }, []);



  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
       <Typography variant="body2">
          Average Download Speed
          <br />
        </Typography>
       <Typography variant="h4" component="div">
          {total_average_download_speed}
           mb/s
        </Typography>
        <AverageWifiChart />
     </CardContent>
   </Card>
 
 );
}
