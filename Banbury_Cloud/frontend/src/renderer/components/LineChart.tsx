import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { LineChart } from '@mui/x-charts/LineChart';
import { Box, Container, Grid, Typography } from "@mui/material";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import PieActiveArc from './Piechart';
import { useAuth } from '../context/AuthContext';



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
  // Add more device properties as needed
}



interface UserResponse {
  devices: Device[];
  first_name: string;
  last_name: string;
  overall_date_added: Date[];
  // Include other fields from your API response as needed
}


export default function DifferentLength() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [UserResponse, setUserResponse] = useState<UserResponse[]>([]);
  const [overallDateAdded, setOverallDateAdded] = useState<Date[]>([]);
  const { username } = useAuth();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<UserResponse>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        const roundedDevices = response.data.devices.map(device => ({
          ...device,
          average_upload_speed: parseFloat(device.average_upload_speed.toFixed(2)),
          average_download_speed: parseFloat(device.average_download_speed.toFixed(2)),
          average_gpu_usage: parseFloat(device.average_gpu_usage.toFixed(2)),
          average_cpu_usage: parseFloat(device.average_cpu_usage.toFixed(2)),
          average_ram_usage: parseFloat(device.average_ram_usage.toFixed(2)),
          date_added: device.date_added.map(dateStr => new Date(dateStr)),
        }));


        // Convert overall_date_added strings to Date objects
        const convertedOverallDates = response.data.overall_date_added.map(dateStr => new Date(dateStr));
        setOverallDateAdded(convertedOverallDates);


        setDevices(roundedDevices);      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);




  const uploadData = devices.map(device => device.upload_network_speed);
  const date_added = devices.map(device => device.date_added);
  const downloadData = devices.map(device => device.download_network_speed);
  const deviceNames = devices.map(device => device.device_name);
  // Concatenate upload network speeds for all devices into a single array
  const uploadSpeeds: number[] = devices.flatMap(device => device.upload_network_speed);
  const downloadSpeeds: number[] = devices.flatMap(device => device.download_network_speed);
  const cpu_usage: number[] = devices.flatMap(device => device.cpu_usage);

  const deviceData = devices.map(device => ({
    name: device.device_name,
    uploadSpeeds: device.upload_network_speed,
    cpuUsage: device.cpu_usage,
    // Include any other device-specific metrics you wish to analyze/plot
  }));


  const xLabels: string[] = Array.from(Array(uploadSpeeds.length).keys()).map(String);



  const downloadMaxLength = devices.reduce((max, device) => Math.max(max, device.cpu_usage.length), 0);
  const downloadlabels: string[] = Array.from({ length: downloadMaxLength }, (_, index) => index.toString());
  const cpuMaxLength = devices.reduce((max, device) => Math.max(max, device.cpu_usage.length), 0);
  const cpulabels: string[] = Array.from({ length: cpuMaxLength }, (_, index) => index.toString());
  const uploadMaxLength = devices.reduce((max, device) => Math.max(max, device.upload_network_speed.length), 0);
  const uploadlabels: string[] = Array.from({ length: uploadMaxLength }, (_, index) => index.toString());
  const totalDates = overallDateAdded.map(date =>
    `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
  );


  // Limit the data points to match the number of dates available
// /*   */ const limitedCpuUsage = cpu_usage.slice(0, totalDates.length);
  // const cpuSeries = [{ data: limitedCpuUsage, label: "CPU Usage" }];

  // Prepare series data for each device for Upload Speeds
  const uploadSeries = devices.map(device => ({
    data: device.upload_network_speed,
    label: device.device_name, // Use the device name as the label for each series
    showMark: false,
  }));


  // Prepare series data for each device for Upload Speeds
  const downloadSeries = devices.map(device => ({
    data: device.download_network_speed,
    label: device.device_name, // Use the device name as the label for each series
    showMark: false,
  }));


  // Prepare series data for each device for CPU Usage
  const cpuSeries = devices.map(device => ({
    data: device.cpu_usage,
    label: device.device_name, 
    showMark: false,

  }));





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
<Grid container spacing={2} columns={16}>
<Grid item xs={8}>
    <Card>
      <CardContent>
      <Box my={0}>
        <Typography variant="h5" gutterBottom>Upload Speeds</Typography>
        <LineChart
          width={500}
          height={300}
          series={uploadSeries}
          xAxis={[{ scaleType: 'point', data: uploadlabels }]}
        />
      </Box>
    </CardContent>
    </Card>
</Grid> 



        
<Grid item xs={8}>
    <Card>
      <CardContent>
 
      <Box my={0}>
        <Typography variant="h5" gutterBottom>Download Speeds</Typography>
        <LineChart
          width={500}
          height={300}
          series={downloadSeries}
          xAxis={[{ scaleType: 'point', data: downloadlabels }]}
        />
      </Box>
     </CardContent>
    </Card>
 
</Grid> 

<Grid item xs={8}>
   <Card>
      <CardContent>

      <Box my={0}>
        <Typography variant="h5" gutterBottom>CPU Usage</Typography>
        <LineChart
          width={500}
          height={300}
          series={cpuSeries}
          xAxis={[{ scaleType: 'point', data: cpulabels }]}
        />
      </Box>
      </CardContent>
    </Card>
 
</Grid> 

</Grid>
    </Container>
  );
}



