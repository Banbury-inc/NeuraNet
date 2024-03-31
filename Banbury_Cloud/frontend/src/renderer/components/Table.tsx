import React, { useEffect, useState, useRef  } from 'react';
import Stack from '@mui/material/Stack';
import { exec } from "child_process";
import axios from 'axios';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import DownloadIcon from '@mui/icons-material/Download';
import TableBody from '@mui/material/TableBody';
import LoadingButton from '@mui/lab/LoadingButton';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Button from '@mui/material/Button';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import DeleteIcon from '@mui/icons-material/Delete';
import FilterListIcon from '@mui/icons-material/FilterList';
import { visuallyHidden } from '@mui/utils';
import { CardContent, Container } from "@mui/material";
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import InputFileUploadButton from './uploadfilebutton';
import AccountMenuIcon from './AccountMenuIcon';
import { useAuth } from '../context/AuthContext';
import Card from '@mui/material/Card';
import { SnackbarProvider, VariantType, useSnackbar } from 'notistack';
import CircularProgress, {
  CircularProgressProps,
} from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';


interface Device {
  id: string;
  name: string;
  files: File[];
}

// Simplified data interface to match your file structure
interface FileData {
  id: number;
  fileName: string;
  dateUploaded: string;
  fileSize: string;
  deviceID: string;
  deviceName: string;
}

// Define head cells according to FileData
const headCells = [
  { id: 'fileName', numeric: false, label: 'Name' },
  { id: 'fileSize', numeric: false, label: 'Size' },
  { id: 'fileSize', numeric: false, label: 'Location' },
  { id: 'dateUploaded', numeric: true, label: 'Date Uploaded' },
];

type Order = 'asc' | 'desc';

interface HeadCell {
  disablePadding?: boolean;
  id: keyof FileData;
  label: string;
  numeric: boolean;
}

interface EnhancedTableProps {
  numSelected: number;
  onRequestSort: (event: React.MouseEvent<unknown>, property: keyof FileData) => void;
  onSelectAllClick: (event: React.ChangeEvent<HTMLInputElement>, checked: boolean) => void;
  order: Order;
  orderBy: keyof FileData;
  rowCount: number;
}


function EnhancedTableHead(props: EnhancedTableProps) {
  const { onSelectAllClick, order, orderBy, numSelected, rowCount, onRequestSort } = props;
  const createSortHandler = (property: keyof FileData) => (event: React.MouseEvent<unknown>) => {
    onRequestSort(event, property);
  };

    
  return (

    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            color="secondary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              'aria-label': 'select all desserts',
            }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? 'right' : 'left'}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

interface EnhancedTableToolbarProps {
  numSelected: number;
}

function EnhancedTableToolbar(props: EnhancedTableToolbarProps) {
  const { numSelected } = props;

  return (
    <Toolbar
      sx={{
        pl: { sm: 2 },
        pr: { xs: 1, sm: 1 },
        ...(numSelected > 0 && {
          bgcolor: (theme) =>
            alpha(theme.palette.primary.main, theme.palette.action.activatedOpacity),
        }),
      }}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{ flex: '1 1 100%' }}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected
        </Typography>
      ) : (
        <Typography
          sx={{ flex: '1 1 100%' }}
          variant="h6"
          id="tableTitle"
          component="div"
        >
       </Typography>
      )}
      {numSelected > 0 ? (
        <Tooltip title="Delete">
          <IconButton>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
}



export default function EnhancedTable() {
  const [order, setOrder] = useState<Order>('asc');
  const [orderBy, setOrderBy] = useState<keyof FileData>('fileName');
  const [selected, setSelected] = useState<readonly number[]>([]);
  const [selectedFileNames, setSelectedFileNames] = useState<string[]>([]);
  const [selectedDeviceNames, setSelectedDeviceNames] = useState<string[]>([]);
  const [hoveredRowId, setHoveredRowId] = useState<number | null>(null);
  const [page, setPage] = useState(0);
  const [dense, setDense] = useState(false);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [fileRows, setFileRows] = useState<FileData[]>([]); // State for storing fetched file data
  const getSelectedFileNames = () => {
    return selected.map(id => {
      const file = fileRows.find(file => file.id === id);
      return file ? file.fileName : null;
    }).filter(fileName => fileName !== null); // Filter out any null values if a file wasn't found
  };

const handleApiCall = async () => {
  const selectedFileNames = getSelectedFileNames();

  // Prepare the request options for fetch
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // Include other headers as needed
    },
    body: JSON.stringify({
      files: selectedFileNames,
    }),
  };

  try {
    const response = await fetch('http://localhost:5000/request_file_test', requestOptions);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Response:', data);
    // Handle your response here
  } catch (error) {
    console.error('API call error:', error);
  }
};


function formatBytes(bytes: number, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

  const [Firstname, setFirstname] = useState<string>('');
  const [Lastname, setLastname] = useState<string>('');
  const { username } = useAuth();
  console.log(username)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[] 
          first_name: string;
          last_name: string;
        // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
        // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');

        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        setFirstname(fetchedFirstname); 
        setLastname(fetchedLastname); 
        const files = response.data.devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex, // Generating unique IDs
            // id: device.id + fileIndex,
            fileName: file["File Name"],
            // fileSize: file["File Size"],
            fileSize: formatBytes(file["File Size"]),
            dateUploaded: file["Date Uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name
          }))
        );

        setFileRows(files);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();

  },

  []);



  useEffect(() => {
    const interval = setInterval(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[] 
          first_name: string;
          last_name: string;
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');

        const fetchedFirstname = response.data.first_name;
        const fetchedLastname = response.data.last_name;
        setFirstname(fetchedFirstname); 
        setLastname(fetchedLastname); 
        const files = response.data.devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex, // Generating unique IDs
            // id: device.id + fileIndex,
            fileName: file["File Name"],
            // fileSize: file["File Size"],
            fileSize: formatBytes(file["File Size"]),
            dateUploaded: file["Date Uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name
          }))
        );

        setFileRows(files);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, 1000); 

  return () => clearInterval(interval);
  },

  []);



  const handleRequestSort = (
    event: React.MouseEvent<unknown>,
    property: keyof FileData,
  ) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const newSelected = fileRows.map((n) => n.id);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event: React.MouseEvent<unknown>, id: number) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected: readonly number[] = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
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

    const fileName = fileRows.find(file => file.id === id)?.fileName;
    const deviceName = fileRows.find(file => file.id === id)?.deviceName;
    const newSelectedFileNames = newSelected.map(id => fileRows.find(file => file.id === id)?.fileName).filter(name => name !== undefined) as string[];
    const newSelectedDeviceNames = newSelected.map(id => fileRows.find(file => file.id === id)?.deviceName).filter(name => name !== undefined) as string[];
    setSelectedFileNames(newSelectedFileNames);
    setSelectedDeviceNames(newSelectedDeviceNames);
    console.log(newSelectedFileNames)
    console.log(selectedFileNames)

  };


  const [buttonText, setButtonText] = useState('Download');
  const [selectedfiles, setSelectedFiles] = useState<readonly number[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const handleDownloadClick = async () => {
    try{
      setLoading(true);

      const scriptPath = 'src/main/download.py'; // Update this to the path of your Python script
       
      exec(`python "${scriptPath}" "${selectedFileNames}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          setLoading(false);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          setLoading(false);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          setLoading(false);
          return
        }
        console.log(`Python Script Message: ${stdout}`);

      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };

  const handleDeleteClick = async () => {
    try{

      const scriptPath = 'src/main/delete.py'; // Update this to the path of your Python script
       
      exec(`python "${scriptPath}" "${selectedFileNames}" "${selectedDeviceNames}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);

      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };


  const handleUploadClick = async () => {
    try{

      const scriptPath = 'src/main/upload.py'; // Update this to the path of your Python script
       
      exec(`python "${scriptPath}" "${selectedFileNames}"`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        if (stderr) {
          console.error(`Python Script Error: ${stderr}`);
          return
        }
        if (stdout) {
          console.log(`Python Script Message: ${stdout}`);
          return
        }
        console.log(`Python Script Message: ${stdout}`);

      });
    } catch (error) {
      console.error('There was an error!', error);
 
    } 
  };



  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChangeDense = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDense(event.target.checked);
  };

  const isSelected = (id: number) => selected.indexOf(id) !== -1;

  // Avoid a layout jump when reaching the last page with empty rows.
  // Calculate empty rows for pagination
  const emptyRows = page > 0 ? Math.max(0, (1 + page) * rowsPerPage - fileRows.length) : 0;

function stableSort<T>(array: T[], comparator: (a: T, b: T) => number): T[] {
  return array
    .map((el, index) => ({ el, index })) // Attach the original index to each element
    .sort((a, b) => {
      const order = comparator(a.el, b.el);
      if (order !== 0) return order; // If elements are not equal, sort them according to `comparator`
      return a.index - b.index; // If elements are equal, sort them according to their original position
    })
    .map(({ el }) => el); // Extract the sorted elements
}

function getComparator<Key extends keyof any>(
  order: Order,
  orderBy: Key,
): (a: { [key in Key]: number | string }, b: { [key in Key]: number | string }) => number {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

function descendingComparator<T>(a: T, b: T, orderBy: keyof T) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function CircularProgressWithLabel(
  props: CircularProgressProps & { value: number },
) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress variant="determinate" {...props} />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography
          variant="caption"
          component="div"
          color="text.secondary"
        >{`${Math.round(props.value)}%`}</Typography>
      </Box>
    </Box>
  );
}


function MyApp() {

  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const [progress, setProgress] = useState(0);
  const [trigger, setTrigger] = useState(false); // State to trigger re-renders
  const timerRef = useRef<number | null>(null); // Ref to store timer

  useEffect(() => {
    timerRef.current = window.setInterval(() => {
      setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
      setTrigger((prevTrigger) => !prevTrigger); // Toggle trigger to force re-render
    }, 1000);
    return () => {
      if (timerRef.current !== null) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const handleClick = async () => {

     enqueueSnackbar('Downloading' + {selectedFileNames}, {
      variant: 'default' as VariantType,
      autoHideDuration: null, // Snackbar will not automatically close
      action: (
        <React.Fragment>
          <CircularProgress value={progress} />
          <Button color="inherit" size="small" onClick={handleClose}>
            Close
          </Button>
        </React.Fragment>
      ),
    });

    await handleDownloadClick();
  };

  const handleClose = () => {
    closeSnackbar();
  };

  return (
    <React.Fragment>
      <Button variant='outlined' size='small' onClick={handleClick}>Download</Button>
    </React.Fragment>
  );
}




function CircularWithValueLabel() {
  const [progress, setProgress] = React.useState(10);

  React.useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
    }, 800);
    return () => {
      clearInterval(timer);
    };
  }, []);

  return <CircularProgressWithLabel value={progress} />;
}


const visibleRows = stableSort(fileRows, getComparator(order, orderBy))
  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);


  return (
    <Container>
      <Box sx={{ width: '100%', mt: 0, pt: 2 }}>
        <Stack spacing={2}>
         <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
            <Grid item>
          <Typography variant="h2" textAlign="left">
            Files
          </Typography>
            </Grid>

           <Grid item>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
                <AccountMenuIcon />
      </Box>
            </Grid>
            </Grid>
 
          <Grid container spacing={2}>
            </Grid>

       </Stack>
<Card variant='outlined'>
<CardContent>
          <Grid container spacing={2}>
            <Grid item>
              <InputFileUploadButton/>

            </Grid>
            <Grid item>
              <LoadingButton variant="outlined" loading={loading} loadingPosition="end" endIcon={<DownloadIcon />} onClick={handleDownloadClick} size="small">
                {/* {buttonText} */}
                {loading ? 'Loading...' : buttonText}
              </LoadingButton>
            </Grid>
            {/* <Grid item> */}
              {/* <SnackbarProvider maxSnack={3}> */}
            {/*   <SnackbarProvider  */}

            {/*       maxSnack={3}  */}
            {/*       anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }} */}
            {/*       TransitionProps={{ */}
            {/*         // Customize your transition props here */}
            {/*         direction: 'up', // Set the direction of the transition */}
            {/*         // timeout: 500, // Set the duration of the transition in milliseconds */}
            {/*       }} */}
            {/*     > */}

            {/*     <MyApp /> */}
            {/*   </SnackbarProvider> */}
            {/* </Grid> */}
            <Grid item>
              <Button variant="outlined" onClick={handleDeleteClick} size="small">
                Delete
              </Button>
            </Grid>
          </Grid>
 
        <Box my={2}>
          {/* <EnhancedTableToolbar numSelected={selected.length} /> */}
          <TableContainer>
            <Table aria-labelledby="tableTitle" size="small">
              <EnhancedTableHead
                numSelected={selected.length}
                order={order}
                orderBy={orderBy}
                onSelectAllClick={handleSelectAllClick}
                onRequestSort={handleRequestSort}
                rowCount={fileRows.length}
              />
              <TableBody>
                {stableSort(fileRows, getComparator(order, orderBy))
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => {
                    const isItemSelected = isSelected(row.id);
                    const labelId = `enhanced-table-checkbox-${index}`;

                    return (
                      <TableRow
                        hover
                        onClick={(event) => handleClick(event, row.id)}
                        role="checkbox"
                        aria-checked={isItemSelected}
                        tabIndex={-1}
                        key={row.id}
                        selected={isItemSelected}
                      onMouseEnter={() => setHoveredRowId(row.id)} // Track hover state
                      onMouseLeave={() => setHoveredRowId(null)} // Clear hover state                onMouseEnter={() => setHoveredRowId(row.id)} // Track hover state
                        sx={{
                          '&:hover .checkbox': {
                            opacity: 1, // Show the checkbox on hover
                          }
                        }}
                      >
                        <TableCell  sx={{ borderBottomColor: "#424242" }} padding="checkbox">
                          {hoveredRowId === row.id ? ( // Only render Checkbox if row is hovered
                          <Checkbox
                            color="primary"
                            checked={isItemSelected}
                            inputProps={{ 'aria-labelledby': labelId }}
                          />
                          ) : null}
                        </TableCell>
                        <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} id={labelId} scope="row" padding="none">
                          {row.fileName}
                        </TableCell>
                        <TableCell align="left" sx={{ borderBottomColor: "#424242" }}>{row.fileSize}</TableCell>
                        <TableCell align="left"  sx={{ borderBottomColor: "#424242" }} >{row.deviceName}</TableCell>
                        <TableCell align="right" sx={{ borderBottomColor: "#424242" }} >{row.dateUploaded}</TableCell>
                      </TableRow>
                    );
                  })}
                {/* Handle empty rows if necessary */}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={fileRows.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Box>
        </CardContent>
        </Card>
      </Box>
    </Container>
  );
}
