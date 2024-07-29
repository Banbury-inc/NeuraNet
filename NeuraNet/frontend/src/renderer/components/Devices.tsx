import { Box, Container, Grid, Typography } from "@mui/material";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import electronLogo from "../../../static/electron.svg";
import DeviceNetworkCard from "./DeviceNetworkCard";
import DeviceNetworkDownloadCard from "./DeviceNetworkDownloadCard";
import DifferentLength from "./LineChart";

import Stack from '@mui/material/Stack';
import DevicesList from "./DevicesList";
import Chip from '@mui/material/Chip';
import Avatar from '@mui/material/Avatar';
import TaskBadge from "./TaskBadge";
import AccountMenuIcon from './AccountMenuIcon';
export default function Greetings(): JSX.Element {


  const [Firstname, setFirstname] = useState<string>('');
  const [Lastname, setLastname] = useState<string>('');
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[] 
          first_name: string;
          last_name: string;
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');

        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        setFirstname(fetchedFirstname); 
        setLastname(fetchedLastname); 
        console.log(fetchedFirstname);
     } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);




  return (

    <Container>
      <Box sx={{ width: '100%', mt: 0 }}>
        <Stack spacing={2}>

         <Grid container justifyContent="space-between" alignItems="center" spacing={2}>

            <Grid item>
          <Typography variant="h2" textAlign="left">
            Files
          </Typography>

            </Grid>

            <Grid item>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
              <Stack direction="row" spacing={0} sx={{ width: '100%' }}>
                <TaskBadge />
                <AccountMenuIcon />
          <Typography variant="h2" textAlign="left">
            Files
          </Typography>


                </Stack>
 
      </Box>
 
            </Grid>

            </Grid>

        <DevicesList />
      <DeviceNetworkCard />
      <DeviceNetworkDownloadCard />
        </Stack>

        </Box>
    </Container>
  );
}
