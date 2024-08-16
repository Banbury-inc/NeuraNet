import { Box, Container, Grid, Typography } from "@mui/material";
import React, { useState } from "react";
import electronLogo from "../../../static/electron.svg";
import DifferentLength from "./LineChart";
import PieActiveArc from "./Piechart";
import BasicCard from "./card";
import Average_Wifi_Speed from "./average_wifi_speed";
import TotalNumberofFiles from "./total_number_of_files";
import TotalNumberofDevices from "./total_number_of_devices";
import Stack from '@mui/material/Stack';
import EnhancedTable from "./Table";
import Button from '@mui/material/Button';
import InputFileUpload from './uploadfilebutton';
import Card from '@mui/material/Card';




export default function Files(): JSX.Element {
  const [buttonText, setButtonText] = useState('Download');
  const handleDownloadClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/request_file', {
        method: 'POST', // or 'POST'
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers your API needs
        },
        // If your API requires a body, uncomment the line below
        body: JSON.stringify({ files: ["file1.txt", "file2.doc"] }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setButtonText(data.message)
      console.log(data);

      // Handle the response data
      // For example, if it's a file to download:
      // window.location.href = data.fileUrl;
    } catch (error) {
      console.error('There was an error!', error);
    }
  };


  return (
        <EnhancedTable  />
  );
}
