
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as net from 'net';
import * as crypto from 'crypto';
import ConfigParser from 'configparser';
import { useAuth } from '../../context/AuthContext';

dotenv.config();

const homeDirectory = os.homedir();
const BANBURY_FOLDER = path.join(homeDirectory, '.banbury');
const CONFIG_FILE = path.join(BANBURY_FOLDER, '.banbury_config.ini');

if (!fs.existsSync(BANBURY_FOLDER)) {
  fs.mkdirSync(BANBURY_FOLDER);
}

if (!fs.existsSync(CONFIG_FILE)) {
  const config = new ConfigParser();
  config.set('banbury_cloud', 'credentials_file', 'credentials.json');
  fs.writeFileSync(CONFIG_FILE, config.toString());
}

function connectToRelayServer(): net.Socket {
  // const RELAY_HOST = '34.28.13.79';
  const RELAY_HOST = '0.0.0.0';
  const RELAY_PORT = 443;
  const senderSocket = new net.Socket();
  senderSocket.connect(RELAY_PORT, RELAY_HOST);
  return senderSocket;
}

function loadCredentials(): Record<string, string> {
  try {
    const config = new ConfigParser();
    config.read(CONFIG_FILE);
    const credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
    const credentialsFilePath = path.join("BCloud", credentialsFile);
    return JSON.parse(fs.readFileSync(credentialsFilePath, 'utf-8'));
  } catch (error) {
    return {};
  }
}

function saveCredentials(credentials: Record<string, string>): void {
  const config = new ConfigParser();
  config.read(CONFIG_FILE);
  const credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
  const credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
  fs.writeFileSync(credentialsFilePath, JSON.stringify(credentials));
}

function old_upload_file(file_path: any) {
  const senderSocket = connectToRelayServer();

  const endOfHeader = Buffer.from('END_OF_HEADER');
  const credentials = loadCredentials();
  let username = Object.keys(credentials)[0];
  const file_size = ""
  let header: string | null = null;
  let buffer = Buffer.alloc(0);

  const directory_name: string = "BCloud";
  const directory_path: string = path.join(os.homedir(), directory_name);

  try {
    fs.copyFileSync(file_path, path.join(directory_path, path.basename(file_path)));
    console.log(`File copied successfully to ${directory_name}`);
  } catch (error) {
    console.log(`Error copying file: ${error}`);
  }

  return '';
}

function upload_file(file_path: any, global_file_path: any) {

  const directory_name: string = "BCloud";
  const directory_path: string = path.join(os.homedir(), directory_name);
  console.log("directory_path", directory_path);
  console.log("file_path", file_path);
  console.log("global_file_path", global_file_path);

  try {
    fs.copyFileSync(file_path, path.join(directory_path, path.basename(file_path)));
    console.log(`File copied successfully to ${directory_name}`);
  } catch (error) {
    console.log(`Error copying file: ${error}`);
  }

  return '';
}





function main(file_path: any, global_file_path: any) {
  const result = upload_file(file_path, file_path);
}

export default main;
