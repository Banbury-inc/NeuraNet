import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';

export default function AverageWifiChart() {
  return (
    <LineChart
      xAxis={[{ data: [1, 2, 3, 5, 8, 10] }]}
      series={[
        {
          data: [30, 40, 80, 30, 50, 100],
        },
      ]}
      width={400}
      height={300}
    />
  );
}
