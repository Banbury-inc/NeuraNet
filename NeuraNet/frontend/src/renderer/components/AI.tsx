import React, { useEffect, useState, useRef } from 'react';
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
import { Skeleton } from '@mui/material';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import HomeIcon from '@mui/icons-material/Home';
import Agents from './AI/agents';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import GrainIcon from '@mui/icons-material/Grain';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import SendIcon from '@mui/icons-material/Send';
import * as path from "path";
import Button from '@mui/material/Button';
import Autocomplete from '@mui/material/Autocomplete';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import Toolbar from '@mui/material/Toolbar';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
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
import { TreeView } from '@mui/x-tree-view';
import AddIcon from '@mui/icons-material/Add';
import NavigateBeforeOutlinedIcon from '@mui/icons-material/NavigateBeforeOutlined';
import NavigateNextOutlinedIcon from '@mui/icons-material/NavigateNextOutlined';
import TextField from '@mui/material/TextField';
import { chat } from './scripts/ai';




import CircularProgress, {
  CircularProgressProps,
} from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import delete_file from './scripts/delete';
import upload_file from './scripts/upload';
import DataManagementCard from './TreeView';
import CustomizedTreeView from './TreeView';
import { NavigateBefore } from '@mui/icons-material';
import TaskBadge from './TaskBadge';


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
  { id: 'location', numeric: false, label: 'Location' },
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

  function handleClick(event: React.MouseEvent<HTMLDivElement, MouseEvent>) {
    event.preventDefault();
    console.info('You clicked a breadcrumb.');
  }



  return (

    <TableHead>
      <TableRow>
        <TableCell colSpan={headCells.length + 1} style={{ padding: 0 }}> {/* Ensure this TableCell spans all columns */}
          <div role="presentation" onClick={handleClick} style={{ display: 'flex', width: '100%' }}>
            <Breadcrumbs aria-label="breadcrumb" style={{ flexGrow: 1 }}>
              <Link
                underline="hover"
                color="inherit"
                href="/"
                style={{ display: 'flex', alignItems: 'center' }}
              >
                <HomeIcon style={{ marginRight: 5 }} fontSize="inherit" />
                Home
              </Link>
              <Link
                underline="hover"
                color="inherit"
                href="/material-ui/getting-started/installation/"
                style={{ display: 'flex', alignItems: 'center' }}
              >
                <WhatshotIcon style={{ marginRight: 5 }} fontSize="inherit" />
                Core
              </Link>
              <Typography
                color="text.primary"
                style={{ display: 'flex', alignItems: 'center' }}
              >
                <GrainIcon style={{ marginRight: 5 }} fontSize="inherit" />
                All Files
              </Typography>
            </Breadcrumbs>
          </div>
        </TableCell>
      </TableRow>
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



export default function AI() {
  const [order, setOrder] = useState<Order>('asc');
  const [orderBy, setOrderBy] = useState<keyof FileData>('fileName');
  const [selected, setSelected] = useState<readonly number[]>([]);
  const [selectedFileNames, setSelectedFileNames] = useState<string[]>([]);
  const [selectedDeviceNames, setSelectedDeviceNames] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
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
  const [messages, setMessages] = useState([
    { id: 0, text: 'Hello! How can I assist you today?', sender: 'bot' }
  ]);
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
        finally {
          setIsLoading(false); // Set loading to false once data is fetched or in case of an error
        }
      };
      fetchData();
    }, 1000);

    return () => clearInterval(interval);
  },

    []);



  const [deleteloading, setdeleteLoading] = useState<boolean>(false);
  const handleDeleteClick = async () => {
    setdeleteLoading(true);
    delete_file(selectedFileNames, selectedDeviceNames);
    setdeleteLoading(false);
    return;
  }
  const handleUploadClick = async () => {
    try {

      const env = process.env.NODE_ENV || 'development';
      let baseDir = '';
      let filename = '';
      let command = '';
      let devbaseDir = '';
      let prodbaseDir = path.join(process.resourcesPath, 'python');
      if (env === 'development') {
        baseDir = devbaseDir;
        filename = 'python/upload.py';
        command = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python3';
      } else if (env === 'production') {
        baseDir = prodbaseDir;
        filename = 'upload.py';
        command = process.platform === 'win32' ? 'Scripts\\python.exe' : 'bin/python3';

      }
      // const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';

      const exactcommand = path.join(baseDir, command);
      const scriptPath = path.join(baseDir, filename);





      exec(`${exactcommand} "${scriptPath}" "${selectedFileNames}"`, (error, stdout, stderr) => {
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
    const [showAgents, setShowAgents] = useState(false); // State to trigger re-renders
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

      enqueueSnackbar('Downloading' + { selectedFileNames }, {
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







  return (
    // <Box sx={{ width: '100%', height: '100%', flexGrow: 1 , pl: 4, pr: 4, mt: 0, pt: 5 }}>
    <Box sx={{
      width: '100%',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      pl: 4,
      pr: 4,
      mt: 0,
      pt: 5,

    }}>
      <Stack spacing={2}>
        <Grid container justifyContent="space-between" alignItems="center" spacing={2}>
          <Grid item>
            <Typography variant="h2" textAlign="left">
              Athena
            </Typography>
          </Grid>

          <Grid item>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
              <Stack direction="row" spacing={0} sx={{ width: '100%' }}>
                <TaskBadge />
                <AccountMenuIcon />
              </Stack>
            </Box>
          </Grid>
        </Grid>

        <Card variant='outlined' sx={{ flexGrow: 0 }}>
          <CardContent>
            <Box sx={{ flex: 1, overflowY: 'auto', mt: 3 }}>
              {messages.map(message => (
                <Typography key={message.id} align={message.sender === 'bot' ? 'left' : 'right'} paragraph>
                  {message.text}
                </Typography>
              ))}
            </Box>
          </CardContent>
        </Card >
        <Card variant='outlined' sx={{ flexGrow: 0 }}>
          <CardContent>
            <Button
              onClick={chat}
            >
              Upload
            </Button>


          </CardContent>
        </Card >



      </Stack>

      <Stack direction="row" spacing={0} sx={{ width: '100%' }}>
      </Stack>


      <Grid container alignItems={"flex-end"} sx={{ mb: 4, pl: 20, pr: 20 }}>
        {/* <Agents />  */}
      </Grid>

      <Grid container alignItems={"flex-end"} sx={{ mb: 4, pl: 20, pr: 20 }}>
        <TextField
          fullWidth
          label="Message Athena"
          size='small'
          InputProps={{
            type: 'search',
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() => console.log('Search icon clicked')}
                  edge="end"
                >
                  <SendIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}


        />
      </Grid>
    </Box>

  );
}
