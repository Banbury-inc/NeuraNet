
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import PieActiveArc from './Piechart';

export default function BasicCard() {
  // Initialize state to store the first name
  const [total_device_storage, set_total_device_storage] = useState('');

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
        set_total_device_storage(last_total_device_storage.toFixed(2))




      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Call fetchData inside useEffect
    fetchData();
  }, []);

  return (
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
  );
}
