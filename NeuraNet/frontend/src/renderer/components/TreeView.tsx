
import * as React from 'react';
import { Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView, TreeItem } from '@mui/x-tree-view';  // Corrected import for TreeView and TreeItem
import Folder from '@mui/icons-material/Folder';
import InsertPhotoOutlinedIcon from '@mui/icons-material/InsertPhotoOutlined';
import ArticleOutlinedIcon from '@mui/icons-material/ArticleOutlined';
import FolderOpenOutlinedIcon from '@mui/icons-material/FolderOpenOutlined';
import MovieOutlinedIcon from '@mui/icons-material/MovieOutlined';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import FolderIcon from '@mui/icons-material/Folder';
import HomeIcon from '@mui/icons-material/Home';
import axios from 'axios';
import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';

// Simplified data interface to match your file structure
interface FileData {
  id: number;
  fileName: string;
  dateUploaded: string;
  filePath: string;
  deviceID: string;
  deviceName: string;
}



export default function CustomizedTreeView() {

  const { username, first_name, last_name, devices, setFirstname, setLastname, setDevices, redirect_to_login, setredirect_to_login } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
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
            filePath: file["file_path"],
            dateUploaded: file["date_uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name
          }))
        );

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
              fileName: file["file_name"],
              // fileSize: file["File Size"],
              filePath: file["file_path"],
              dateUploaded: file["date_uploaded"],
              deviceID: device.device_number,
              deviceName: device.device_name
            }))
          );

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






  return (
    <Box sx={{ width: '100%', height: '100%', mr: 4 }}>
      <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ width: '100%', height: 240, flexGrow: 1, overflowY: 'auto' }}
      >
        <TreeItem nodeId="1" label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <HomeIcon style={{ marginRight: 5 }} fontSize="inherit" />
            <Typography variant="inherit" sx={{ ml: 1, fontWeight: 'medium' }}>All files</Typography>
          </Box>
        }>
          <TreeItem nodeId="2" label={
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Folder style={{ marginRight: 5 }} fontSize="inherit" />
              <Typography variant="inherit" sx={{ ml: 1 }}>chamonix</Typography>
            </Box>
          } />
        </TreeItem>
        <TreeItem nodeId="5" label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <ArticleOutlinedIcon style={{ marginRight: 5 }} fontSize="inherit" />
            <Typography variant="inherit" sx={{ ml: 1, fontWeight: 'medium' }}>Documents</Typography>
          </Box>
        }>
          <TreeItem nodeId="10" label={
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <InsertPhotoOutlinedIcon style={{ marginRight: 5 }} fontSize="inherit" />
              <Typography variant="inherit" sx={{ ml: 1 }}>Photos</Typography>
            </Box>
          } />
          <TreeItem nodeId="6" label={
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Folder style={{ marginRight: 5 }} fontSize="inherit" />
              <Typography variant="inherit" sx={{ ml: 1 }}>MUI</Typography>
            </Box>
          }>
            <TreeItem nodeId="8" label={
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Folder style={{ marginRight: 5 }} fontSize="inherit" />
                <Typography variant="inherit" sx={{ ml: 1 }}>index.js</Typography>
              </Box>
            } />
          </TreeItem>
        </TreeItem>
        <TreeItem nodeId="3" label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <MovieOutlinedIcon style={{ marginRight: 5 }} fontSize="inherit" />
            <Typography variant="inherit" sx={{ ml: 1, fontWeight: 'medium' }}>Videos</Typography>
          </Box>
        }>
          <TreeItem nodeId="4" label={
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Folder style={{ marginRight: 5 }} fontSize="inherit" />
              <Typography variant="inherit" sx={{ ml: 1 }}>Chamonix</Typography>
            </Box>
          } />
        </TreeItem>
        <TreeItem nodeId="9" label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>

            <AutoAwesomeIcon style={{ marginRight: 5 }} fontSize="inherit" />
            <Typography variant="inherit" sx={{ ml: 1, fontWeight: 'medium' }}>AI</Typography>
          </Box>
        }>
          <TreeItem nodeId="10" label={
            <Box sx={{ display: 'flex', alignItems: 'center' }}>

              <Folder style={{ marginRight: 5 }} fontSize="inherit" />
              <Typography variant="inherit" sx={{ ml: 1 }}>Agent</Typography>
            </Box>
          } />
        </TreeItem>
      </TreeView>    </Box>
  );
}

