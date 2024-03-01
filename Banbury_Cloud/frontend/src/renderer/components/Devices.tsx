import { Box, Container, Grid, Typography } from "@mui/material";
import React from "react";
import electronLogo from "../../../static/electron.svg";
import DeviceNetworkCard from "./DeviceNetworkCard";
import DeviceNetworkDownloadCard from "./DeviceNetworkDownloadCard";
import DifferentLength from "./LineChart";

import Stack from '@mui/material/Stack';
import DevicesList from "./DevicesList";


export default function Greetings(): JSX.Element {
  return (
    <Container>
      <Grid container justifyContent="left">
      </Grid>
 
      <Typography variant="h2" textAlign="left">
        Devices
      </Typography>
      <Stack spacing={4}>
        <DevicesList />
      <DeviceNetworkCard />
      <DeviceNetworkDownloadCard />
        </Stack>
    </Container>
  );
}
