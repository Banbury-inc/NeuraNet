import * as React from 'react';
import { Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView, TreeItem } from '@mui/x-tree-view';  // Corrected import for TreeView and TreeItem
import Folder from '@mui/icons-material/Folder';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

interface FileData {
  id: number;
  fileType: string;
  fileName: string;
  dateUploaded: string;
  fileSize: string;
  filePath: string;
  fileParent: string;
  deviceID: string;
  deviceName: string;
  children?: FileData[];
}

function formatBytes(bytes: number, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function buildTree(files: FileData[]): FileData[] {
  const map = new Map<string, FileData>();

  // Only map directories
  files.filter(file => file.fileType === 'directory').forEach(file => {
    map.set(file.filePath, { ...file, children: [] });
  });

  const roots: FileData[] = [];

  map.forEach(file => {
    const parent = map.get(file.fileParent);
    if (parent) {
      parent.children?.push(file);
    } else {
      roots.push(file);
    }
  });

  return roots;
}

export default function CustomizedTreeView() {
  const { username, first_name, last_name, global_file_path, devices, setFirstname, setLastname, setGlobal_file_path, setDevices, redirect_to_login, setredirect_to_login } = useAuth();
  const [fileRows, setFileRows] = useState<FileData[]>([]); // State for storing fetched file data

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<{
          devices: any[],
          first_name: string,
          last_name: string
        }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');

        const { first_name, last_name, devices } = response.data;
        setFirstname(first_name);
        setLastname(last_name);

        const files = devices.flatMap((device, index) =>
          device.files.map((file: any, fileIndex: number): FileData => ({
            id: index * 1000 + fileIndex, // Generating unique IDs
            fileType: file["file_type"],
            fileName: file["file_name"],
            fileSize: formatBytes(file["file_size"]),
            filePath: file["file_path"],
            dateUploaded: file["date_uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name,
            fileParent: file["file_parent"]
          }))
        );

        setFileRows(buildTree(files));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, [username, setFirstname, setLastname]);

  useEffect(() => {
    const interval = setInterval(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get<{
            devices: any[],
            first_name: string,
            last_name: string
          }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');

          const { first_name, last_name, devices } = response.data;
          setFirstname(first_name);
          setLastname(last_name);

          const files = devices.flatMap((device, index) =>
            device.files.map((file: any, fileIndex: number): FileData => ({
              id: index * 1000 + fileIndex, // Generating unique IDs
              fileType: file["file_type"],
              fileName: file["file_name"],
              fileSize: formatBytes(file["file_size"]),
              filePath: file["file_path"],
              dateUploaded: file["date_uploaded"],
              deviceID: device.device_number,
              deviceName: device.device_name,
              fileParent: file["file_parent"]
            }))
          );

          setFileRows(buildTree(files));
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };

      fetchData();
    }, 1000);

    return () => clearInterval(interval);
  }, [username, setFirstname, setLastname]);

  const handleNodeSelect = (event: React.SyntheticEvent, nodeId: string) => {
    const findNodeById = (nodes: FileData[], id: number): FileData | null => {
      for (const node of nodes) {
        if (node.id === id) {
          return node;
        }
        if (node.children) {
          const childNode = findNodeById(node.children, id);
          if (childNode) {
            return childNode;
          }
        }
      }
      return null;
    };

    const selectedNode = findNodeById(fileRows, parseInt(nodeId));
    if (selectedNode) {
      setGlobal_file_path(selectedNode.filePath); // Set the global file path
    }
  };

  const renderTreeItems = (nodes: FileData[]) => {
    return nodes.map((node) => (
      <TreeItem
        key={node.id}
        nodeId={String(node.id)}
        label={
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Folder style={{ marginRight: 5 }} fontSize="inherit" />
            <Typography variant="inherit" sx={{ ml: 1 }}>{node.fileName}</Typography>
          </Box>
        }
      >
        {node.children && renderTreeItems(node.children)}
      </TreeItem>
    ));
  };

  return (
    <Box sx={{ width: '100%', height: '100%', mr: 4 }}>
      <TreeView
        aria-label="file system navigator"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ width: '100%', height: 240, flexGrow: 1, overflowY: 'auto' }}
        onNodeSelect={handleNodeSelect}
      >
        {renderTreeItems(fileRows)}
      </TreeView>
      {global_file_path && (
        <Typography variant="body1" sx={{ mt: 2 }}>
          Selected Directory: {global_file_path}
        </Typography>
      )}
    </Box>
  );
}

