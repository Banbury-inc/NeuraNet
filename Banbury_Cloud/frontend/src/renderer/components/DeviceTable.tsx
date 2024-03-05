import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import DeleteIcon from '@mui/icons-material/Delete';
import FilterListIcon from '@mui/icons-material/FilterList';
import { Container, Typography, Grid, Button } from "@mui/material";
import Chip from '@mui/material/Chip';
import Avatar from '@mui/material/Avatar';
import { Stack } from '@mui/material';
import LineChart from './LineChart';




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
  // Include other fields from your API response as needed
}

export default function DevicesTable() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

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
          average_ram_usage: parseFloat(device.average_ram_usage.toFixed(2)),
          date_added: device.date_added.map(dateStr => new Date(dateStr)),
        }));
        setDevices(roundedDevices);      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = devices.map((device) => device.device_number);
      setSelected(newSelected);
    } else {
      setSelected([]);
    }
  };

  const handleClick = (event: React.MouseEvent<unknown>, device_number: number) => {
    const selectedIndex = selected.indexOf(device_number);
    let newSelected: number[] = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, device_number);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1),
      );
    }
    setSelected(newSelected);
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const isSelected = (device_number: number) => selected.indexOf(device_number) !== -1;


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
            Devices
          </Typography>

            </Grid>
            <Grid item>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
        <Chip avatar={<Avatar>{Firstname.charAt(0)}</Avatar>} label={`${Firstname} ${Lastname}`} />
      </Box>

            </Grid>
            </Grid>

          <Grid container spacing={1}>
            <Grid item>
              <Button variant="outlined" size="small">Add Device</Button>
            </Grid>
            <Grid item>
              <Button variant="outlined" size="small">Remove Device</Button>
            </Grid>
          </Grid>
      </Stack>

        <Box my={2}>
            <TableContainer>
              <Table sx={{ minWidth: 750 }} size="small">
                <TableHead>
                  <TableRow>
                    <TableCell padding="checkbox">
                      <Checkbox
                        color="primary"
                        indeterminate={selected.length > 0 && selected.length < devices.length}
                        checked={devices.length > 0 && selected.length === devices.length}
                        onChange={handleSelectAllClick}
                        inputProps={{ 'aria-label': 'select all devices' }}
                      />
                    </TableCell>
                    <TableCell>Name</TableCell>
                    <TableCell>IP Address</TableCell>
                    <TableCell>Total Storage</TableCell>
                    <TableCell>Avg. Upload Speed</TableCell>
                    <TableCell>Avg. Download Speed</TableCell>
                    <TableCell>Avg. GPU usage</TableCell>
                    <TableCell>Avg. CPU usage</TableCell>
                    <TableCell>Avg. RAM usage</TableCell>
                    {/* Add more table headers as needed */}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {(rowsPerPage > 0
                    ? devices.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    : devices
                  ).map((device) => {
                    const isItemSelected = isSelected(device.device_number);
                    const labelId = `enhanced-table-checkbox-${device.device_number}`;

                    return (
                      <TableRow
                        hover
                        onClick={(event) => handleClick(event, device.device_number)}
                        role="checkbox"
                        aria-checked={isItemSelected}
                        tabIndex={-1}
                        key={device.device_number}
                        selected={isItemSelected}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            color="primary"
                            checked={isItemSelected}
                            inputProps={{ 'aria-labelledby': labelId }}
                          />
                        </TableCell>
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.device_name}
                        </TableCell>

                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.ip_address}
                        </TableCell>

                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.storage_capacity_GB}
                        </TableCell>
 

                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.average_upload_speed}
                        </TableCell>
 
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.average_download_speed}
                        </TableCell>
 
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.average_gpu_usage}
                        </TableCell>
 
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.average_cpu_usage}
                        </TableCell>
 
                        <TableCell component="th" id={labelId} scope="row" padding="none">
                          {device.average_ram_usage}
                        </TableCell>
 

                        {/* Render other device details here */}
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25]}
              component="div"
              count={devices.length}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          <LineChart />
        </Box>
      </Box>
    </Container>
  );
}

