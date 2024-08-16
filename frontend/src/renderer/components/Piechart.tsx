
import { PieChart } from '@mui/x-charts/PieChart';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Container, Grid, Typography } from '@mui/material';
import { useAuth } from '../context/AuthContext';
import {
  blueberryTwilightPalette,
  mangoFusionPalette,
  cheerfulFiestaPalette,
}
 from '@mui/x-charts/colorPalettes';

interface Device {
  device_name: string;
  storage_capacity_GB: number;
}

interface UserResponse {
  devices: Device[];
  overall_date_added: Date[];
}

const PieActiveArc: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [overallDateAdded, setOverallDateAdded] = useState<Date[]>([]);
  const { username } = useAuth();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<UserResponse>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        const roundedDevices = response.data.devices.map(device => ({
          ...device,
          storage_capacity_GB: parseFloat(device.storage_capacity_GB.toFixed(2)),
        }));

        // Convert overall_date_added strings to Date objects
        const convertedOverallDates = response.data.overall_date_added.map(dateStr => new Date(dateStr));
        setOverallDateAdded(convertedOverallDates);

        setDevices(roundedDevices);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const totalStorage = devices.reduce((total, device) => total + device.storage_capacity_GB, 0);

  const data = devices.map(device => ({
    id: device.device_name,
    // value: (device.storage_capacity_GB / totalStorage) * 100,
    value: device.storage_capacity_GB,
    label: device.device_name,
    tooltipValue: device.storage_capacity_GB + ' GB',
  }));

  const categories = {
    blueberryTwilight: blueberryTwilightPalette,
    mangoFusion: mangoFusionPalette,
    cheerfulFiesta: cheerfulFiestaPalette,
  } as const;

  type PaletteKey = keyof typeof categories;

  const [colorScheme, setColorScheme] = useState<PaletteKey>('blueberryTwilight');
  const customColorPalette = ['#FAE1DC',  '#FF4500','#0000F5', '#FF4500', '#51DA4C', '#0000FF', '#FFF639', '#FF45FF', '#FE7600', '#8A2BE2', '#A0522D'];
  return (
      <PieChart
        colors={categories[colorScheme]}
        // colors={customColorPalette}
        series={[
          {
            data,
            highlightScope: { faded: 'global', highlighted: 'item' },
            faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
          },
        ]}
        slotProps={{
          legend: {
            direction: 'row',
            position: { vertical: 'bottom', horizontal: 'left' },
            padding: 0,
          },
        }}
      sx={{ marginLeft: '100px', marginTop: '-100px'}}
      />
  );
};

export default PieActiveArc;

