
import * as React from 'react';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { Card } from '@mui/material';





function createData(
  name: string,
  calories: number,
  fat: number,
  carbs: number,
) {
  return {
    name,
    calories,
    fat,
    carbs,
    history: [
      {
        date: '2020-01-05',
        customerId: '11091700',
        amount: 3,
      },
      {
        date: '2020-01-02',
        customerId: 'Anonymous',
        amount: 1,
      },
    ],
  };
}

function Row(props: { row: ReturnType<typeof createData> }) {
  const { row } = props;
  const [open, setOpen] = React.useState(false);

  return (
    <React.Fragment>
      <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>

          <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
          <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            {row.name}
            </TableCell>
 
          <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            {row.calories}
            </TableCell>
 

          <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            {row.fat}
            </TableCell>
 

             <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            {row.carbs}
            </TableCell>
 
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box sx={{ margin: 1 }}>
              <Typography variant="h6" gutterBottom component="div">
                History
              </Typography>
              <Table size="small" aria-label="purchases">
                <TableHead>
                  <TableRow>
                    <TableCell>Pending Tasks</TableCell>
                    <TableCell>Completed Tasks</TableCell>
                    <TableCell align="right">Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {row.history.map((historyRow) => (
                    <TableRow key={historyRow.date}>
                      <TableCell component="th" scope="row">
                        {historyRow.date}
                      </TableCell>
                      <TableCell>{historyRow.customerId}</TableCell>
                      <TableCell align="right">{historyRow.amount}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );
}

const rows = [
  createData('Main Agent', 159, 6.0, 24),
  createData('Critic Agent', 237, 9.0, 37),
  createData('Research Agent', 262, 16.0, 24),
  createData('Health Agent', 305, 3.7, 67),
];

export default function Agents() {
  return (

<Card variant='outlined' sx={{ flexGrow: 0 }}>
    <TableContainer>
      <Table aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            Agents
            </TableCell>
            <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            Pending Tasks
            </TableCell>
            <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            Completed Tasks
            </TableCell>
             <TableCell component="th"  sx={{ borderBottomColor: "#424242" }} scope="row" padding="none">
            Status
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <Row key={row.name} row={row} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    </Card>
  );
}
