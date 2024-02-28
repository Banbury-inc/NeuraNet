import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import {
  blueberryTwilightPalette,
  mangoFusionPalette,
  cheerfulFiestaPalette,
} from '@mui/x-charts/colorPalettes';

const data = [

  { id: 0, value: 10, label: 'Desktop' },
  { id: 1, value: 15, label: 'Macbook Pro' },
  { id: 2, value: 20, label: 'Linux-Workstation' },
];

const categories = {
  blueberryTwilight: blueberryTwilightPalette,
  mangoFusion: mangoFusionPalette,
  cheerfulFiesta: cheerfulFiestaPalette,
} as const;

type PaletteKey = keyof typeof categories;
export default function PieActiveArc() {
    const [colorScheme, setColorScheme] =
    React.useState<PaletteKey>('blueberryTwilight');
  return (
    <PieChart
      colors={categories[colorScheme]}
      series={[
        {
          data,
          highlightScope: { faded: 'global', highlighted: 'item' },
          faded: { innerRadius: 30, additionalRadius: -30, color: 'gray' },
        },
      ]}
      height={100}
      width={400}
    />
  );
}
