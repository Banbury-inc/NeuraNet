import React, { useEffect, useState, useRef } from 'react';
import os from 'os';
import { ipcRenderer } from 'electron';
import Stack from '@mui/material/Stack';
import { exec } from "child_process";
import { join } from 'path';
import { shell } from 'electron';
import isEqual from 'lodash/isEqual';
import axios from 'axios';
import { useMediaQuery } from '@mui/material';
import ButtonBase from '@mui/material/ButtonBase';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import { readdir, stat } from 'fs/promises';
import Table from '@mui/material/Table';
import DownloadIcon from '@mui/icons-material/Download';
import fs from 'fs';
import TableBody from '@mui/material/TableBody';
import LoadingButton from '@mui/lab/LoadingButton';
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import DevicesIcon from '@mui/icons-material/Devices';
import TableCell from '@mui/material/TableCell';

import TableContainer from '@mui/material/TableContainer';
import CreateNewFolderOutlinedIcon from '@mui/icons-material/CreateNewFolderOutlined';
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
import NewInputFileUploadButton from './newuploadfilebutton';
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
import { get_current_date_and_time, get_device_name, get_directory_info } from './scripts/receiver';
import { UpdateDevices } from './scripts/update_devices';
import upload_file from './scripts/upload';
import DataManagementCard from './TreeView';
import CustomizedTreeView from './TreeView';
import { BorderLeft, NavigateBefore } from '@mui/icons-material';
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


interface SmallDeviceInfo {
  user: string;
  device_number: number;
  device_name: string;
  files: FileInfo[];
  date_added: string;
}


interface FileInfo {
  File_Type: string;
  File_Name: string;
  Kind: string;
  Date_Uploaded: string;
  File_Size: number;
  File_Priority: number;
  File_Path: string;
  Original_Device: string;
}
const headCells: HeadCell[] = [
  { id: 'fileName', numeric: false, label: 'Name', isVisibleOnSmallScreen: true },
  { id: 'fileSize', numeric: false, label: 'Size', isVisibleOnSmallScreen: true },
  { id: 'kind', numeric: false, label: 'Kind', isVisibleOnSmallScreen: true },
  { id: 'deviceName', numeric: false, label: 'Location', isVisibleOnSmallScreen: false },
  { id: 'available', numeric: true, label: 'Status', isVisibleOnSmallScreen: false },
  { id: 'dateUploaded', numeric: true, label: 'Date Uploaded', isVisibleOnSmallScreen: false },
];

type Order = 'asc' | 'desc';

interface HeadCell {
  disablePadding?: boolean;
  id: keyof FileData;
  label: string;
  numeric: boolean;
  isVisibleOnSmallScreen: boolean;
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
  const isSmallScreen = useMediaQuery('(max-width:960px)');
  const createSortHandler = (property: keyof FileData) => (event: React.MouseEvent<unknown>) => {
    onRequestSort(event, property);
  };

  function handleClick(event: React.MouseEvent<HTMLDivElement, MouseEvent>) {
    event.preventDefault();
    console.info('You clicked a breadcrumb.');
  }


  const { global_file_path, global_file_path_device } = useAuth();  // Assuming global_file_path is available via context

  const pathSegments = global_file_path ? global_file_path.split('/').filter(Boolean) : []; // Split and remove empty segments safely

  // Function to handle breadcrumb click, might need more logic to actually navigate
  const handleBreadcrumbClick = (path: string) => {
    console.info(`Navigate to: ${path}`);
    // Set global_file_path or navigate logic here
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell colSpan={headCells.length + 1} style={{ padding: 0 }}>
          <div style={{ display: 'flex', width: '100%' }}>
            <Breadcrumbs aria-label="breadcrumb" style={{ flexGrow: 1 }}>
              <Link
                underline="hover"
                color="inherit"
                href="#"
                onClick={() => handleBreadcrumbClick('/')}
                style={{ display: 'flex', alignItems: 'center' }}
              >
                <GrainIcon style={{ marginRight: 5 }} fontSize="inherit" />
                Core
              </Link>
              {global_file_path_device && (  // Only render if global_file_path_device has a value
                <Link
                  underline="hover"
                  color="inherit"
                  href="#"
                  onClick={() => handleBreadcrumbClick(global_file_path_device)}  // Pass the device path to the handler
                  style={{ display: 'flex', alignItems: 'center' }}
                >
                  <DevicesIcon style={{ marginRight: 5 }} fontSize="inherit" />
                  {global_file_path_device}
                </Link>
              )}
              {pathSegments.map((segment, index) => {
                const pathUpToSegment = '/' + pathSegments.slice(0, index + 1).join('/');
                return (
                  <Link
                    key={index}
                    underline="hover"
                    color="inherit"
                    href="#"
                    onClick={() => handleBreadcrumbClick(pathUpToSegment)}
                    style={{ display: 'flex', alignItems: 'center' }}
                  >
                    {segment}
                  </Link>
                );
              })}
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
        {headCells
          .filter(headCell => !isSmallScreen || headCell.isVisibleOnSmallScreen)
          .map(headCell => (
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



export default function EnhancedTable() {
  const isSmallScreen = useMediaQuery('(max-width:960px)');
  const [order, setOrder] = useState<Order>('asc');
  const [orderBy, setOrderBy] = useState<keyof FileData>('fileName');
  const [selected, setSelected] = useState<readonly number[]>([]);
  const [selectedFileNames, setSelectedFileNames] = useState<string[]>([]);
  const [selectedDeviceNames, setSelectedDeviceNames] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [hoveredRowId, setHoveredRowId] = useState<number | null>(null);
  const [page, setPage] = useState(0);
  const [dense, setDense] = useState(false);
  const [rowsPerPage, setRowsPerPage] = useState(100);
  const [fileRows, setFileRows] = useState<FileData[]>([]); // State for storing fetched file data
  const [allFiles, setAllFiles] = useState<FileData[]>([]);
  const { global_file_path, global_file_path_device, setGlobal_file_path } = useAuth();
  const [isAddingFolder, setIsAddingFolder] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");
  const [disableFetch, setDisableFetch] = useState(false);
  const { updates, setUpdates, username, first_name, last_name, devices, setFirstname, setLastname, setDevices, redirect_to_login, setredirect_to_login } = useAuth();
  const getSelectedFileNames = () => {
    return selected.map(id => {
      const file = fileRows.find(file => file.id === id);
      return file ? file.fileName : null;
    }).filter(fileName => fileName !== null); // Filter out any null values if a file wasn't found
  };


  function formatBytes(bytes: number, decimals: number = 2): string {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  console.log(username)

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

        if (disableFetch) {
          return;
        }
        else {
          setAllFiles(files);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [updates]);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;
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

        const newFiles = devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number) => ({
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

        if (!disableFetch) {
          if (!isEqual(newFiles, allFiles)) {
            console.log("Updating files...");
            setAllFiles(newFiles);


          } else {
            console.log("No changes in files.");
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
    intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, [username, disableFetch, allFiles]); // Include allFiles in the dependency array


  useEffect(() => {
    const pathToShow = global_file_path || '/';
    const pathSegments = pathToShow.split('/').filter(Boolean).length;

    const filteredFiles = allFiles.filter(file => {
      if (!global_file_path && !global_file_path_device) {
        return true; // Show all files
      }

      if (!global_file_path && global_file_path_device) {
        return file.deviceName === global_file_path_device; // Show all files for the specified device
      }

      const fileSegments = file.filePath.split('/').filter(Boolean).length;
      const isInSameDirectory = file.filePath.startsWith(pathToShow) && fileSegments === pathSegments + 1;
      const isFile = file.filePath === pathToShow && file.kind !== 'Folder';

      return isInSameDirectory || isFile;
    });

    setFileRows(filteredFiles);

  }, [global_file_path, global_file_path_device, allFiles]);


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

    const newSelectedFilePaths = newSelected
      .map(id => fileRows.find(file => file.id === id)?.filePath)
      .filter(name => name !== undefined) as string[];

    console.log(newSelectedFilePaths[0]);




    // Assuming the directory structure is based on `BCloud` in user's home directory
    //
    const directoryName = "BCloud";
    const directoryPath = join(os.homedir(), directoryName);


    let fileFound = false;
    let folderFound = false;
    let filePath = '';

    try {

      const fileStat = await stat(newSelectedFilePaths[0]);
      if (fileStat.isFile()) {
        fileFound = true;
        console.log(`File '${fileName}' found in directory.`);
      }
      if (fileStat.isDirectory()) {
        folderFound = true;
        setGlobal_file_path(newSelectedFilePaths[0]);
      }
      if (fileFound) {
        // Send an IPC message to the main process to handle opening the file
        console.log(`Opening file '${fileName}'...`);
        shell.openPath(newSelectedFilePaths[0]);
      }
      if (folderFound) {
        // Send an IPC message to the main process to handle opening the file
        console.log(`Opening folder '${fileName}'...`);
        // shell.openPath(newSelectedFilePaths[0]);
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
    const deletePromises: Promise<void>[] = [];  // Array to hold promises for deletion operations

    selectedFileNames.forEach((fileName: string) => {
      const currentPath: string = global_file_path ?? '';
      const filePath: string = path.join(currentPath, fileName);
      console.log(filePath);

      // Create a promise for each file operation and push it to the array
      const deletePromise = new Promise<void>((resolve, reject) => {
        fs.stat(filePath, (err: NodeJS.ErrnoException | null, stats: fs.Stats) => {
          if (err) {
            console.error(`Error reading file stats: ${err}`);
            reject(err);
            return;
          }
          if (stats.isDirectory()) {
            fs.rmdir(filePath, { recursive: true }, (err: NodeJS.ErrnoException | null) => {
              if (err) {
                console.error(`Error deleting directory: ${err}`);
                reject(err);
              } else {
                console.log(`Directory '${fileName}' deleted successfully at ${filePath}`);
                resolve();
              }
            });
          } else if (stats.isFile()) {
            fs.unlink(filePath, (err: NodeJS.ErrnoException | null) => {
              if (err) {
                console.error(`Error deleting file: ${err}`);
                reject(err);
              } else {
                console.log(`File '${fileName}' deleted successfully at ${filePath}`);
                resolve();
              }
            });
          }
        });
      });

      deletePromises.push(deletePromise);
    });

    try {
      // Wait for all delete operations to complete
      await Promise.all(deletePromises);
      console.log('All files deleted successfully.');
    } catch (error) {
      console.error('Error deleting files:', error);
    }

    setdeleteLoading(false);
    setIsAddingFolder(false);
    setNewFolderName("");
    setDisableFetch(false);

    // Run update devices function after all deletions are complete
    const update_result = await UpdateDevices(username);
    console.log(update_result);
    setUpdates(updates + 1);
  };

  const [backHistory, setBackHistory] = useState<any[]>([]);
  const [forwardHistory, setForwardHistory] = useState<any[]>([]);

  const handleBackClick = async () => {
    if (global_file_path) {
      const newPath = global_file_path.substring(0, global_file_path.lastIndexOf('/'));
      setBackHistory([...backHistory, global_file_path]); // Add current path to back history
      setGlobal_file_path(newPath);
      setForwardHistory([]); // Clear forward history
      console.log(backHistory);
    } else {
      console.warn("Global file path is not defined or is null");
    }
  };

  const handleForwardClick = async () => {
    if (backHistory.length > 0) {
      const lastBackPath = backHistory[backHistory.length - 1];
      setBackHistory(backHistory.slice(0, -1)); // Remove the last back path
      setForwardHistory([global_file_path, ...forwardHistory]); // Add current path to forward history
      setGlobal_file_path(lastBackPath);
    } else {
      console.warn("No back history available");
    }
  };
  const handleAddFolderClick = async () => {
    console.log("Add folder clicked")
    setDisableFetch(true);
    setIsAddingFolder(true);
    setNewFolderName(""); // Reset folder name input
    setFileRows((prevFileRows) => [
      ...prevFileRows,
      {
        // id: prevFileRows.length + 1, // Assign a unique ID for the new folder
        id: Date.now(), // Assign a unique ID for the new folder
        fileName: "",
        fileSize: "",
        kind: "Folder",
        dateUploaded: new Date().toISOString(),
        filePath: "",
        deviceID: "",
        deviceName: "",
        helpers: 0,
        available: "Available",
      },
    ]);
  };


  const handleFolderNameSave = async () => {
    if (newFolderName.trim() === "") {
      setIsAddingFolder(false);
      setUpdates(updates + 1);
      return; // Exit if the folder name is empty
    }

    const currentPath = global_file_path ?? '';
    const newFolderPath = path.join(currentPath, newFolderName);

    // Attempt to create the folder on the filesystem or backend here
    try {
      if (!fs.existsSync(newFolderPath)) {
        fs.mkdirSync(newFolderPath);
        console.log(`Folder created at ${newFolderPath}`);

        // Update the temporary folder row to reflect the new folder
        setFileRows(prevFileRows => prevFileRows.map(row =>
          row.kind === "Folder" && row.fileName === ""
            ? { ...row, fileName: newFolderName, filePath: newFolderPath }
            : row
        ));
      }
    } catch (error) {
      console.error('Error creating folder:', error);
    }
    console.log(updates)
    setIsAddingFolder(false);
    setNewFolderName("");
    setDisableFetch(false);

    const update_result = await UpdateDevices(username);
    console.log(update_result)
    setUpdates(updates + 1);
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

  const handleBlur = async () => {
    if (newFolderName.trim() !== "") {
      await handleFolderNameSave();
    }
    setIsAddingFolder(false);
  };


  const handleKeyPress = async (e: any) => {
    if (e.key === "Enter") {
      await handleFolderNameSave();
      setIsAddingFolder(false);
      console.log(isAddingFolder);
    }
  };
  return (
    // <Box sx={{ width: '100%', pl: 4, pr: 4, mt: 0, pt: 5 }}>
    <Box sx={{ width: '100%', pt: 0 }}>

      {/* <Stack spacing={2}> */}
      {/*   <Grid container justifyContent="space-between" alignItems="center" spacing={2}> */}
      {/*     <Grid item> */}
      {/*       <Typography variant="h2" textAlign="left"> */}
      {/*         Files */}
      {/*       </Typography> */}
      {/*     </Grid> */}

      {/*     <Grid item> */}
      {/*       <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}> */}
      {/*         <Stack direction="row" spacing={0} sx={{ width: '100%' }}> */}
      {/*           <TaskBadge /> */}
      {/*           <AccountMenuIcon /> */}
      {/*         </Stack> */}
      {/*       </Box> */}
      {/*     </Grid> */}

      {/*   </Grid> */}

      {/*   <Grid container spacing={2}> */}
      {/*   </Grid> */}

      {/* </Stack> */}

      <Card variant='outlined' sx={{ borderTop: 0, borderLeft: 0, borderBottom: 0 }}>
        <CardContent sx={{ paddingBottom: '2px !important', paddingTop: '46px' }}>
          <Stack spacing={2} direction="row" sx={{ flexWrap: 'nowrap' }}>
            <Grid container spacing={0} sx={{ display: 'flex', flexWrap: 'nowrap', pt: 0 }}>
              <Grid item paddingRight={1}>
                <Tooltip title="Navigate back">
                  <Button
                    onClick={handleBackClick}

                    sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed
                  >
                    <NavigateBeforeOutlinedIcon
                      fontSize="inherit"
                    />
                  </Button>
                </Tooltip>
              </Grid>
              <Grid item paddingRight={1}>
                <Tooltip title="Navigate forward">
                  <Button
                    onClick={handleForwardClick}

                    sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed
                  >
                    <NavigateNextOutlinedIcon
                      fontSize="inherit"
                    />
                  </Button>
                </Tooltip>
              </Grid>

              <Grid item paddingRight={1}>
                <Tooltip title="New folder">
                  <Button
                    onClick={handleAddFolderClick}
                    sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed
                  >
                    <CreateNewFolderOutlinedIcon
                      fontSize="inherit"
                    />
                  </Button>
                </Tooltip>
              </Grid>

              <Grid item paddingRight={1}>
                <Tooltip title="Upload">
                  <NewInputFileUploadButton />
                </Tooltip>
              </Grid>
              <Grid item paddingRight={1}>
                <Tooltip title="Download">
                  <Button
                    onClick={handleDownloadClick}
                    sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed
                  >
                    <DownloadIcon
                      fontSize="inherit"
                    />
                  </Button>
                </Tooltip>
              </Grid>

              {/* <Grid item paddingRight={1}> */}
              {/*   <Tooltip title="Share"> */}
              {/*     <Button */}
              {/*       onClick={handleDownloadClick} */}
              {/*       sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed */}
              {/*     > */}
              {/*       <PersonAddAlt1Icon */}
              {/*         fontSize="inherit" */}
              {/*       /> */}
              {/*     </Button> */}
              {/*   </Tooltip> */}
              {/* </Grid> */}

              <Grid item paddingRight={1}>
                <Tooltip title="Delete">
                  <Button
                    onClick={handleDeleteClick}
                    sx={{ paddingLeft: '4px', paddingRight: '4px', minWidth: '30px' }} // Adjust the left and right padding as needed
                  >
                    <DeleteIcon
                      fontSize="inherit"
                    />
                  </Button>
                </Tooltip>
              </Grid>
            </Grid>
            <Grid container justifyContent='flex-end' alignItems='flex-end'>
              {/* <Grid item> */}
              {/*   <Stack spacing={0} sx={{ width: 300, justifyContent: 'center', mt: 0 }}> */}
              {/*     <Autocomplete */}
              {/*       freeSolo */}
              {/*       fullWidth */}
              {/*       id="free-solo-2-demo" */}
              {/*       disableClearable */}
              {/*       options={top100Films.map((option: any) => option.title)} */}

              {/*       renderInput={(params: any) => ( */}
              {/*         <TextField */}
              {/*           {...params} */}
              {/*           fullWidth */}
              {/*           label="Search input" */}
              {/*           size='small' */}
              {/*           InputProps={{ */}
              {/*             ...params.InputProps, */}
              {/*             type: 'search', */}
              {/*             endAdornment: ( */}
              {/*               <InputAdornment position="end"> */}
              {/*                 <IconButton */}
              {/*                   onClick={() => console.log('Search icon clicked')} */}
              {/*                   edge="end" */}
              {/*                 > */}
              {/*                   <SearchIcon /> */}
              {/*                 </IconButton> */}
              {/*               </InputAdornment> */}
              {/*             ), */}
              {/*           }} */}


              {/*         /> */}
              {/*       )} */}
              {/*     /> */}
              {/*   </Stack> */}
              {/* </Grid> */}
              <Grid item>
                {/* <TaskBadge /> */}
              </Grid>
              <Grid item>

                <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-end' }}>
                  <Stack direction="row">
                    {/* <TaskBadge /> */}
                    <AccountMenuIcon />
                  </Stack>
                </Box>
              </Grid>


            </Grid>
          </Stack>
        </CardContent>
      </Card>
      <Stack direction="row" spacing={0} sx={{ width: '100%', height: '95vh', overflow: 'hidden' }}>
        <Card variant="outlined" sx={{ overflow: 'auto', borderLeft: 0, borderRight: 0 }}>
          <CardContent>
            <Grid container spacing={4}>
              <Grid item>
                <CustomizedTreeView />
              </Grid>
            </Grid>
          </CardContent>
        </Card>
        <Card variant="outlined" sx={{ flexGrow: 1, height: '100%', width: '100%', overflow: 'hidden' }}>
          <CardContent sx={{ height: '100%', width: '100%', overflow: 'auto' }}>
            <Box my={0}>
              <TableContainer sx={{ maxHeight: '90%', overflowY: 'auto', overflowX: 'auto' }}>
                <Table aria-labelledby="tableTitle" size="small">
                  <EnhancedTableHead numSelected={selected.length}
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
                                  sx={{
                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',

                                  }}
                                  component="th"
                                  id={labelId}
                                  scope="row"
                                  padding="normal"
                                >
                                  {row.kind === "Folder" && isAddingFolder && row.fileName === "" ? (
                                    <TextField
                                      value={newFolderName}
                                      size="small"
                                      onChange={(e) => setNewFolderName(e.target.value)}
                                      onBlur={handleFolderNameSave}
                                      onKeyPress={e => {
                                        if (e.key === "Enter") {
                                          e.preventDefault();
                                          handleFolderNameSave();
                                        }
                                      }}
                                      placeholder="Enter folder name"
                                      fullWidth
                                      autoFocus
                                    />
                                  ) : (
                                    <ButtonBase
                                      onClick={(event) => {
                                        event.stopPropagation();
                                        handleFileNameClick(row.id);
                                      }}
                                      style={{ textDecoration: 'none' }}
                                    >
                                      {row.fileName}
                                    </ButtonBase>
                                  )}
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

                                {(!isSmallScreen || headCells.find(cell => cell.id === 'deviceName')?.isVisibleOnSmallScreen) && (
                                  <TableCell align="left" sx={{
                                    borderBottomColor: "#424242",
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',


                                  }} >{row.deviceName}
                                  </TableCell>
                                )}

                                {/* <TableCell */}
                                {/*   padding="normal" */}
                                {/*   align="right" sx={{ */}

                                {/*     borderBottomColor: "#424242", */}
                                {/*     whiteSpace: 'nowrap', */}
                                {/*     overflow: 'hidden', */}
                                {/*     textOverflow: 'ellipsis', */}
                                {/*   }} >{row.helpers}</TableCell> */}



                                {(!isSmallScreen || headCells.find(cell => cell.id === 'available')?.isVisibleOnSmallScreen) && (
                                  <TableCell
                                    align="right"
                                    padding="normal"
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
                                )}

                                {(!isSmallScreen || headCells.find(cell => cell.id === 'dateUploaded')?.isVisibleOnSmallScreen) && (
                                  <TableCell
                                    padding="normal"
                                    align="right" sx={{

                                      borderBottomColor: "#424242",
                                      whiteSpace: 'nowrap',
                                      overflow: 'hidden',
                                      textOverflow: 'ellipsis',
                                    }} >{row.dateUploaded}</TableCell>
                                )}




                              </TableRow>
                            );
                          })
                      )}
                  </TableBody>
                </Table>
              </TableContainer>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25, 50, 100]}
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
