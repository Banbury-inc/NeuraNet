import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import { Box, height } from '@mui/system';

export default function TotalFilesChart() {
  return (
    <Box sx={{height: '70%'}}>
    <LineChart
      xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
      series={[
        {
          data: [200, 500, 550, 700, 600, 800],
        },
      ]}
      // width={800}
      //
      //
      //
      // height={375}
    />
    </Box>
  );
}
