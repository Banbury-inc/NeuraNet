import * as React from 'react';
import { Typography, Box } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import { TreeView, TreeItem } from '@mui/x-tree-view';
import Folder from '@mui/icons-material/Folder';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

interface FileData {
  id: string;
  fileType: string;
  fileName: string;
  dateUploaded: string;
  fileSize: string;
  filePath: string;
  fileParent: string;
  deviceID: string;
  deviceName: string;
  children?: FileData[];
  original_device: string;
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
  const deviceMap = new Map<string, FileData>();
  const roots: FileData[] = [];

  files.forEach(file => {
    if (!deviceMap.has(file.original_device)) {
      const deviceNode: FileData = {
        id: `device-${file.original_device}`,
        fileType: 'directory',
        fileName: file.deviceName,
        dateUploaded: '',
        fileSize: '',
        filePath: '',
        fileParent: '',
        deviceID: file.deviceID,
        deviceName: file.deviceName,
        children: [],
        original_device: file.original_device,
      };
      deviceMap.set(file.original_device, deviceNode);
      roots.push(deviceNode);
    }
  });

  files.forEach(file => {
    const deviceNode = deviceMap.get(file.original_device);
    if (deviceNode) {
      const parent = files.find(f => f.filePath === file.fileParent);
      if (parent) {
        parent.children = parent.children || [];
        parent.children.push(file);
      } else {
        deviceNode.children?.push(file);
      }
    }
  });

  return roots;
}

export default function CustomizedTreeView() {
  const { global_file_path, username, setFirstname, setLastname, setGlobal_file_path } = useAuth();
  const [fileRows, setFileRows] = useState<FileData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/${username}/`);
        const { first_name, last_name, devices } = response.data;
        setFirstname(first_name);
        setLastname(last_name);

        const files = devices.flatMap((device: any, index: any) =>
          device.files.map((file: any, fileIndex: any): FileData => ({
            id: `device-${device.device_number}-file-${fileIndex}`,
            fileType: file["file_type"],
            fileName: file["file_name"],
            fileSize: formatBytes(file["file_size"]),
            filePath: file["file_path"],
            dateUploaded: file["date_uploaded"],
            deviceID: device.device_number,
            deviceName: device.device_name,
            fileParent: file["file_parent"],
            original_device: file["original_device"]
          }))
        );

        setFileRows(buildTree(files));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, [username, setFirstname, setLastname]);

  const handleNodeSelect = (event: React.SyntheticEvent, nodeId: string) => {
    const findNodeById = (nodes: FileData[], id: string): FileData | null => {
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

    const selectedNode = findNodeById(fileRows, nodeId);
    if (selectedNode) {
      setGlobal_file_path(selectedNode.filePath);
    }
  };

  const renderTreeItems = (nodes: FileData[]) => {
    return nodes.map((node) => (
      <TreeItem
        key={node.id}
        nodeId={node.id}
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
        sx={{ width: '100%', flexGrow: 1, overflowY: 'auto' }}
        onNodeSelect={handleNodeSelect}
      >
        {renderTreeItems(fileRows)}
      </TreeView>
    </Box>
  );
}
