import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { LineChart } from '@mui/x-charts/LineChart';
import { Box, Container, Grid, Typography } from "@mui/material";




interface Device {
  device_number: number;
  device_name: string;
  storage_capacity_GB: string;
  average_cpu_usage: number;
  average_download_speed: number;
  average_gpu_usage: number;
  average_ram_usage: number;
  average_time_online: number;
  average_upload_speed: number;
  cpu_usage: number[];
  date_added: string[];
  device_priority: number;
  download_network_speed: number[];
  gpu_usage: number[];
  ip_address: string;
  network_reliability: number;
  optimization_status: boolean;
  ram_usage: number[];
  sync_status: boolean;
  upload_network_speed: number[];
  // Add more device properties as needed
}



interface UserResponse {
  devices: Device[];
  first_name: string;
  last_name: string;
  // Include other fields from your API response as needed
}


export default function DifferentLength() {
  const [devices, setDevices] = useState<Device[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<UserResponse>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');
        const roundedDevices = response.data.devices.map(device => ({
          ...device,
          average_upload_speed: parseFloat(device.average_upload_speed.toFixed(2)),
          average_download_speed: parseFloat(device.average_download_speed.toFixed(2)),
          average_gpu_usage: parseFloat(device.average_gpu_usage.toFixed(2)),
          average_cpu_usage: parseFloat(device.average_cpu_usage.toFixed(2)),
          average_ram_usage: parseFloat(device.average_ram_usage.toFixed(2))
        }));
        setDevices(roundedDevices);      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);




  const uploadData = devices.map(device => device.upload_network_speed);
  const downloadData = devices.map(device => device.download_network_speed);
  const deviceNames = devices.map(device => device.device_name);
  // Concatenate upload network speeds for all devices into a single array
  const uploadSpeeds: number[] = devices.flatMap(device => device.upload_network_speed);
  const cpu_usage: number[] = devices.flatMap(device => device.cpu_usage);

  const xLabels: string[] = Array.from(Array(uploadSpeeds.length).keys()).map(String);
const uData = [4000, 3000, 2000, 2780, 1890, 2390, 3490];
const pData = [2400, 1398, 9800, 3908, 4800, 3800, 4300];
// const xLabels = [
//   'Page A',
//   'Page B',
//   'Page C',
//   'Page D',
//   'Page E',
//   'Page F',
//   'Page G',
// ];


  return (
    <Container>
      <Box my={0}>
        <Typography variant="h5" gutterBottom>Upload Speeds</Typography>
        <LineChart
          width={500}
          height={300}
          series={[{ data: uploadSpeeds, label: 'Upload Speed' }]}
          xAxis={[{ scaleType: 'point', data: xLabels }]}
        />
      </Box>
      <Box my={4}>
        <Typography variant="h5" gutterBottom>CPU Usage</Typography>
        <LineChart
          width={500}
          height={300}
          series={[{ data: cpu_usage, label: 'CPU Usage ' }]}
          xAxis={[{ scaleType: 'point', data: xLabels }]}
        />
      </Box>
 
    </Container>
  );
}

