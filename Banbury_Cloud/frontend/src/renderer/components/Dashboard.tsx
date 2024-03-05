import { Box, Container, Grid, Typography } from "@mui/material";
import React from "react";
import electronLogo from "../../../static/electron.svg";
import DifferentLength from "./LineChart";
import PieActiveArc from "./Piechart";
import BasicCard from "./card";
import Average_Wifi_Speed from "./average_wifi_speed";
import TotalNumberofFiles from "./total_number_of_files";
import TotalNumberofDevices from "./total_number_of_devices";
import Stack from '@mui/material/Stack';

export default function Dashboard(): JSX.Element {
  return (
    <Container>

      <Box sx={{ width: '100%', mt: 0, pt: 4 }}>
    <Stack spacing={1}>
      <Typography variant="h2" textAlign="left">
        Dashboard
      </Typography>


      <Grid container spacing={4}>
        <Grid item>
         <BasicCard />
         </Grid>

        <Grid item>
     <TotalNumberofDevices />

         </Grid>
        <Grid item>
     <TotalNumberofFiles />

         </Grid>
        <Grid item>
     <Average_Wifi_Speed />

         </Grid>
     </Grid>
     </Stack>
     </Box>
    </Container>
  );
}
