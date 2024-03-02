import React, { useEffect, useState } from 'react';
import Stack from '@mui/material/Stack';
import { exec } from "child_process";
import axios from 'axios';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import InputFileUpload from './uploadfilebutton';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Button from '@mui/material/Button';
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
import { Container } from "@mui/material";



// Simplified data interface to match your file structure
interface FileData {
  id: number;
  fileName: string;
  dateUploaded: string;
  fileSize: number;
}

// Define head cells according to FileData
const headCells = [
  { id: 'fileName', numeric: false, label: 'Name' },
  { id: 'fileSize', numeric: false, label: 'File Size (bytes)' },
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
            color="primary"
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


  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{ devices: any[] }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');

        const files = response.data.devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex, // Generating unique IDs
            fileName: file["File Name"],
            fileSize: file["File Size"],
            dateUploaded: file["Date Uploaded"],
          }))
        );
        console.log(files);
        setFileRows(files);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);



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
    const newSelectedFileNames = newSelected.map(id => fileRows.find(file => file.id === id)?.fileName).filter(name => name !== undefined) as string[];
    setSelectedFileNames(newSelectedFileNames);
    console.log(newSelectedFileNames)
    console.log(selectedFileNames)

  };


  const [buttonText, setButtonText] = useState('Download');
  const [selectedfiles, setSelectedFiles] = useState<readonly number[]>([]);
  const handleDownloadClick = async () => {
    try{

      const scriptPath = 'src/main/download.py'; // Update this to the path of your Python script
       
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

  const handleDeleteClick = async () => {
    try{

      const scriptPath = 'src/main/delete.py'; // Update this to the path of your Python script
       
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



const visibleRows = stableSort(fileRows, getComparator(order, orderBy))
  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);


  return (
    <Container>
    <Box 
      gap={4}
      sx={{ width: '100%' }}>
      <Container>
      <Stack spacing={2}>
      <Typography variant="h2" textAlign="left">
        Files
      </Typography>
          <Grid container spacing={1}>
              <Grid item>
                <InputFileUpload />
              </Grid>
              <Grid item>
                <Button 
                variant="outlined"
                onClick={handleDownloadClick}
                size="small"
              >{buttonText}</Button>
              </Grid>
              <Grid item>
                <Button 
                variant="outlined"
                onClick={handleDeleteClick}
                size="small"
              >Delete</Button>
              </Grid>
        </Grid>

      </Stack>
    </Container>

      <Box 
          my={2}
          sx={{ width: '100%'}}>
        <Container>
        <EnhancedTableToolbar numSelected={selected.length} />
        <TableContainer>
          <Table
            sx={{ minWidth: 750 }}
            aria-labelledby="tableTitle"
            size="small"
          >
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
        >
          <TableCell padding="checkbox">
            <Checkbox
              color="primary"
              checked={isItemSelected}
              inputProps={{ 'aria-labelledby': labelId }}
            />
          </TableCell>
          <TableCell component="th" id={labelId} scope="row" padding="none">
            {row.fileName}
          </TableCell>
          <TableCell align="left">{row.fileSize}</TableCell>
          <TableCell align="right">{row.dateUploaded}</TableCell>
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

      </Container>
      </Box>
    </Box>

    </Container>
  );

}
