import React, { useEffect, useState, useRef } from 'react';
import os from 'os';
import { ipcRenderer } from 'electron';
import Stack from '@mui/material/Stack';
import { exec } from "child_process";
import { join } from 'path';
import { shell } from 'electron';
import axios from 'axios';
import ButtonBase from '@mui/material/ButtonBase';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import { readdir, stat } from 'fs/promises';
import Table from '@mui/material/Table';
import DownloadIcon from '@mui/icons-material/Download';
import TableBody from '@mui/material/TableBody';
import LoadingButton from '@mui/lab/LoadingButton';
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import { Skeleton } from '@mui/material';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import HomeIcon from '@mui/icons-material/Home';
import WhatshotIcon from '@mui/icons-material/Whatshot';
import GrainIcon from '@mui/icons-material/Grain';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
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





import CircularProgress, {
  CircularProgressProps,
} from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import delete_file from './scripts/delete';
import { download_file } from './scripts/download_file';
import upload_file from './scripts/upload';
import DataManagementCard from './TreeView';
import CustomizedTreeView from './TreeView';
import { NavigateBefore } from '@mui/icons-material';
import TaskBadge from './TaskBadge';


interface Device {
  id: string;
  name: string;
  online: boolean;
  files: File[];
}

// Simplified data interface to match your file structure
interface FileData {
  id: number;
  fileName: string;
  kind: string;
  dateUploaded: string;
  fileSize: string;
  filePath: string;
  deviceID: string;
  deviceName: string;
  helpers: number;
  available: string;
}

const headCells: HeadCell[] = [
  { id: 'fileName', numeric: false, label: 'Name' },
  { id: 'fileSize', numeric: false, label: 'Size' },
  { id: 'dateUploaded', numeric: false, label: 'Kind' },
  { id: 'deviceName', numeric: false, label: 'Location' },
  { id: 'helpers', numeric: true, label: 'Helpers' },
  { id: 'available', numeric: true, label: 'Status' },
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
              onClick={createSortHandler(headCell.id)}
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
  const [isLoading, setIsLoading] = useState(true);
  const [hoveredRowId, setHoveredRowId] = useState<number | null>(null);
  const [page, setPage] = useState(0);
  const [dense, setDense] = useState(false);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [fileRows, setFileRows] = useState<FileData[]>([]); // State for storing fetched file data
  const [allFiles, setAllFiles] = useState<FileData[]>([]);
  const { global_file_path } = useAuth();
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

  const { username, first_name, last_name, devices, setFirstname, setLastname, setDevices, redirect_to_login, setredirect_to_login } = useAuth();
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

        // const fetchedFirstname = response.data.first_name;
        // const fetchedLastname = response.data.last_name;
        const { first_name, last_name, devices } = response.data;
        setFirstname(first_name);
        setLastname(last_name);
        const files = devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex, // Generating unique IDs
            // id: device.id + fileIndex,
            fileName: file["file_name"],
            // fileSize: file["File Size"],
            kind: file["kind"],
            fileSize: formatBytes(file["file_size"]),
            filePath: file["file_path"],
            dateUploaded: file["date_uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name,
            helpers: 0,
            available: device.online || 0 > 1 ? "Available" : "Unavailable",
          }))
        );
        // const filteredFiles = files.filter(file => file.filePath.startsWith(global_file_path || ''));
        const screencastsPath = '/home/mmills/BCloud/Screencasts';
        const filteredFiles = files.filter(file => file.filePath.startsWith(screencastsPath));
        // setFileRows(files);
        setFileRows(filteredFiles);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();

  },

    []);



  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[];
          first_name: string;
          last_name: string;
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');

        const { first_name, last_name, devices } = response.data;
        setFirstname(first_name);
        setLastname(last_name);

        const helpersCount: Record<string, number> = {};

        const files = devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex,
            fileName: file["file_name"],
            fileSize: formatBytes(file["file_size"]),
            kind: file["kind"],
            filePath: file["file_path"],
            dateUploaded: file["date_uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name,
            helpers: 0,
            available: device.online || 0 > 1 ? "Available" : "Unavailable",
          }))
        );

        setAllFiles(files);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [username, setFirstname, setLastname]);

  useEffect(() => {
    const pathToShow = global_file_path || '/';
    const filteredFiles = allFiles.filter(file => file.filePath.startsWith(pathToShow));
    setFileRows(filteredFiles);
  }, [global_file_path, allFiles]);


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
  const handleFileNameClick = async (id: number) => {
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

    const fileName = fileRows.find(file => file.id === id)?.fileName;
    const newSelectedFileNames = newSelected
      .map(id => fileRows.find(file => file.id === id)?.fileName)
      .filter(name => name !== undefined) as string[];

    console.log(newSelectedFileNames);

    // Assuming the directory structure is based on `BCloud` in user's home directory
    const directoryName = "BCloud";
    const directoryPath = join(os.homedir(), directoryName);

    let fileFound = false;
    let filePath = '';

    try {
      const files = await readdir(directoryPath);

      for (const file of files) {
        const fullPath = join(directoryPath, file);
        const fileStat = await stat(fullPath);

        if (fileStat.isFile() && file === fileName) {
          fileFound = true;
          console.log(`File '${fileName}' found in directory.`);
          filePath = fullPath;
          break;
        }
      }

      if (fileFound) {
        // Send an IPC message to the main process to handle opening the file
        console.log(`Opening file '${fileName}'...`);
        shell.openPath(filePath);
      } else {
        console.error(`File '${fileName}' not found in directory.`);
      }
    } catch (err) {
      console.error('Error searching for file:', err);
    }
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
    setSelectedFiles(selected);
    console.log(selectedFileNames)
    console.log("handling download click")
    let result = download_file(selectedFileNames, selectedDeviceNames);
    console.log(result)


  };

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

  const top100Films = [
    { title: 'The Shawshank Redemption', year: 1994 },
    { title: 'The Godfather', year: 1972 },
    { title: 'The Godfather: Part II', year: 1974 },
    { title: 'The Dark Knight', year: 2008 },
    { title: '12 Angry Men', year: 1957 },
    { title: "Schindler's List", year: 1993 },
    { title: 'Pulp Fiction', year: 1994 },
    {
      title: 'The Lord of the Rings: The Return of the King',
      year: 2003,
    },
    { title: 'The Good, the Bad and the Ugly', year: 1966 },
    { title: 'Fight Club', year: 1999 },
    {
      title: 'The Lord of the Rings: The Fellowship of the Ring',
      year: 2001,
    },
    {
      title: 'Star Wars: Episode V - The Empire Strikes Back',
      year: 1980,
    },
    { title: 'Forrest Gump', year: 1994 },
    { title: 'Inception', year: 2010 },
    {
      title: 'The Lord of the Rings: The Two Towers',
      year: 2002,
    },
    { title: "One Flew Over the Cuckoo's Nest", year: 1975 },
    { title: 'Goodfellas', year: 1990 },
    { title: 'The Matrix', year: 1999 },
    { title: 'Seven Samurai', year: 1954 },
    {
      title: 'Star Wars: Episode IV - A New Hope',
      year: 1977,
    },
    { title: 'City of God', year: 2002 },
    { title: 'Se7en', year: 1995 },
    { title: 'The Silence of the Lambs', year: 1991 },
    { title: "It's a Wonderful Life", year: 1946 },
    { title: 'Life Is Beautiful', year: 1997 },
    { title: 'The Usual Suspects', year: 1995 },
    { title: 'Léon: The Professional', year: 1994 },
    { title: 'Spirited Away', year: 2001 },
    { title: 'Saving Private Ryan', year: 1998 },
    { title: 'Once Upon a Time in the West', year: 1968 },
    { title: 'American History X', year: 1998 },
    { title: 'Interstellar', year: 2014 },
    { title: 'Casablanca', year: 1942 },
    { title: 'City Lights', year: 1931 },
    { title: 'Psycho', year: 1960 },
    { title: 'The Green Mile', year: 1999 },
    { title: 'The Intouchables', year: 2011 },
    { title: 'Modern Times', year: 1936 },
    { title: 'Raiders of the Lost Ark', year: 1981 },
    { title: 'Rear Window', year: 1954 },
    { title: 'The Pianist', year: 2002 },
    { title: 'The Departed', year: 2006 },
    { title: 'Terminator 2: Judgment Day', year: 1991 },
    { title: 'Back to the Future', year: 1985 },
    { title: 'Whiplash', year: 2014 },
    { title: 'Gladiator', year: 2000 },
    { title: 'Memento', year: 2000 },
    { title: 'The Prestige', year: 2006 },
    { title: 'The Lion King', year: 1994 },
    { title: 'Apocalypse Now', year: 1979 },
    { title: 'Alien', year: 1979 },
    { title: 'Sunset Boulevard', year: 1950 },
    {
      title: 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
      year: 1964,
    },
    { title: 'The Great Dictator', year: 1940 },
    { title: 'Cinema Paradiso', year: 1988 },
    { title: 'The Lives of Others', year: 2006 },
    { title: 'Grave of the Fireflies', year: 1988 },
    { title: 'Paths of Glory', year: 1957 },
    { title: 'Django Unchained', year: 2012 },
    { title: 'The Shining', year: 1980 },
    { title: 'WALL·E', year: 2008 },
    { title: 'American Beauty', year: 1999 },
    { title: 'The Dark Knight Rises', year: 2012 },
    { title: 'Princess Mononoke', year: 1997 },
    { title: 'Aliens', year: 1986 },
    { title: 'Oldboy', year: 2003 },
    { title: 'Once Upon a Time in America', year: 1984 },
    { title: 'Witness for the Prosecution', year: 1957 },
    { title: 'Das Boot', year: 1981 },
    { title: 'Citizen Kane', year: 1941 },
    { title: 'North by Northwest', year: 1959 },
    { title: 'Vertigo', year: 1958 },
    {
      title: 'Star Wars: Episode VI - Return of the Jedi',
      year: 1983,
    },
    { title: 'Reservoir Dogs', year: 1992 },
    { title: 'Braveheart', year: 1995 },
    { title: 'M', year: 1931 },
    { title: 'Requiem for a Dream', year: 2000 },
    { title: 'Amélie', year: 2001 },
    { title: 'A Clockwork Orange', year: 1971 },
    { title: 'Like Stars on Earth', year: 2007 },
    { title: 'Taxi Driver', year: 1976 },
    { title: 'Lawrence of Arabia', year: 1962 },
    { title: 'Double Indemnity', year: 1944 },
    {
      title: 'Eternal Sunshine of the Spotless Mind',
      year: 2004,
    },
    { title: 'Amadeus', year: 1984 },
    { title: 'To Kill a Mockingbird', year: 1962 },
    { title: 'Toy Story 3', year: 2010 },
    { title: 'Logan', year: 2017 },
    { title: 'Full Metal Jacket', year: 1987 },
    { title: 'Dangal', year: 2016 },
    { title: 'The Sting', year: 1973 },
    { title: '2001: A Space Odyssey', year: 1968 },
    { title: "Singin' in the Rain", year: 1952 },
    { title: 'Toy Story', year: 1995 },
    { title: 'Bicycle Thieves', year: 1948 },
    { title: 'The Kid', year: 1921 },
    { title: 'Inglourious Basterds', year: 2009 },
    { title: 'Snatch', year: 2000 },
    { title: '3 Idiots', year: 2009 },
    { title: 'Monty Python and the Holy Grail', year: 1975 },
  ];



  return (
    <Box sx={{ width: '100%', pl: 4, pr: 4, mt: 0, pt: 5 }}>
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
              </Stack>
            </Box>
          </Grid>

        </Grid>

        <Grid container spacing={2}>
        </Grid>

      </Stack>
      <Card variant='outlined' sx={{ flexGrow: 0 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item>
              <LoadingButton
                variant="outlined"
                loading={deleteloading}
                loadingPosition="end"
                // endIcon={<NavigateBeforeOutlinedIcon />}
                onClick={handleDeleteClick} size="small">
                {/* {buttonText} */}
                {deleteloading ? '' : "<"}
              </LoadingButton>
            </Grid>

            <Grid item>
              <LoadingButton
                variant="outlined"
                loading={deleteloading}
                loadingPosition="end"
                // endIcon={<NavigateNextOutlinedIcon />}
                onClick={handleDeleteClick} size="small">
                {/* {buttonText} */}
                {deleteloading ? '' : ">"}
              </LoadingButton>
            </Grid>

            <Grid item>
              <LoadingButton
                variant="outlined"
                loading={deleteloading}
                loadingPosition="end"
                endIcon={<AddIcon />}
                onClick={handleDeleteClick} size="small">
                {/* {buttonText} */}
                {deleteloading ? 'Loading...' : "Folder"}
              </LoadingButton>
            </Grid>

            <Grid item>
              <InputFileUploadButton />

            </Grid>
            {/* // download button */}
            <Grid item>
              <LoadingButton variant="outlined" loading={loading} loadingPosition="end"
                endIcon={<DownloadIcon />} onClick={handleDownloadClick} size="small">
                {/* {buttonText} */}
                {loading ? 'Loading...' : buttonText}
              </LoadingButton>
            </Grid>


            <Grid item>
              <LoadingButton
                variant="outlined"
                loading={deleteloading}
                loadingPosition="end"
                endIcon={<PersonAddAlt1Icon />}
                onClick={handleDeleteClick} size="small">
                {/* {buttonText} */}
                {deleteloading ? 'Loading...' : "Share"}
              </LoadingButton>
            </Grid>

            <Grid item>
              <LoadingButton
                variant="outlined"
                loading={deleteloading}
                loadingPosition="end"
                endIcon={<DeleteIcon />}
                onClick={handleDeleteClick} size="small">
                {/* {buttonText} */}
                {deleteloading ? 'Loading...' : "Delete"}
              </LoadingButton>
            </Grid>



            <Grid item>
              <Stack spacing={2} sx={{ width: 300 }}>
                <Autocomplete
                  freeSolo
                  fullWidth
                  id="free-solo-2-demo"
                  disableClearable
                  options={top100Films.map((option: any) => option.title)}

                  renderInput={(params: any) => (
                    <TextField
                      {...params}
                      fullWidth
                      label="Search input"
                      size='small'
                      InputProps={{
                        ...params.InputProps,
                        type: 'search',
                        endAdornment: (
                          <InputAdornment position="end">
                            <IconButton
                              onClick={() => console.log('Search icon clicked')}
                              edge="end"
                            >
                              <SearchIcon />
                            </IconButton>
                          </InputAdornment>
                        ),
                      }}


                    />
                  )}
                />
              </Stack>
            </Grid>

          </Grid>

        </CardContent>
      </Card>
      <Stack direction="row" spacing={0} sx={{ width: '100%', overflow: 'hidden' }}>
        <Card variant='outlined' sx={{ overflow: 'hidden' }}>
          <CardContent>
            <Grid container spacing={4}>
              <Grid item>
                <CustomizedTreeView />
              </Grid>
            </Grid>

          </CardContent>
        </Card>

        <Card variant='outlined' sx={{ flexGrow: 1 }}>
          <CardContent>

            <Box my={0}>
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
                    {
                      isLoading ? (
                        Array.from(new Array(rowsPerPage)).map((_, index) => (
                          <TableRow key={index}>
                            <TableCell padding="checkbox">
                              <Skeleton variant="rectangular" width={24} height={24} />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>
                            <TableCell>
                              <Skeleton variant="text" width="100%" />
                            </TableCell>



                          </TableRow>
                        ))
                      ) : (
                        stableSort(fileRows, getComparator(order, orderBy))
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
                                <TableCell sx={{ borderBottomColor: "#424242" }} padding="checkbox">
                                  {hoveredRowId === row.id ? ( // Only render Checkbox if row is hovered
                                    <Checkbox
                                      color="primary"
                                      checked={isItemSelected}
                                      inputProps={{ 'aria-labelledby': labelId }}
                                    />
                                  ) : null}
                                </TableCell>
                                <TableCell
                                  component="th" sx={{
                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    mr: 2
                                  }}
                                  id={labelId} scope="row" padding="none">
                                  <ButtonBase // Make filename text clickable
                                    onClick={(event) => {
                                      event.stopPropagation(); // Prevent row click event propagation
                                      handleFileNameClick(row.id); // Handle filename click
                                    }}
                                    style={{ textDecoration: 'none' }} // Remove underline
                                  >
                                    {row.fileName}
                                  </ButtonBase>
                                </TableCell>
                                <TableCell
                                  align="left"
                                  padding="normal"

                                  sx={{
                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                  }}>{row.fileSize}</TableCell>
                                <TableCell align="left" sx={{
                                  borderBottomColor: "#424242",
                                  whiteSpace: 'nowrap',
                                  overflow: 'hidden',
                                  textOverflow: 'ellipsis',


                                }} >{row.kind}</TableCell>
                                <TableCell align="left" sx={{
                                  borderBottomColor: "#424242",
                                  whiteSpace: 'nowrap',
                                  overflow: 'hidden',
                                  textOverflow: 'ellipsis',


                                }} >{row.deviceName}</TableCell>

                                <TableCell
                                  padding="normal"
                                  align="right" sx={{

                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                  }} >{row.helpers}</TableCell>
                                <TableCell
                                  padding="normal"
                                  align="right"
                                  sx={{
                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    color: row.available === "Available" ? '#1DB954' : row.available === "Unavailable" ? 'red' : 'inherit',  // Default color is 'inherit'
                                  }}
                                >
                                  {row.available}
                                </TableCell>
                                <TableCell

                                  padding="normal"
                                  align="right" sx={{

                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                  }} >{row.dateUploaded}</TableCell>





                              </TableRow>
                            );
                          })
                      )}
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
      </Stack>
    </Box >

  );
}
