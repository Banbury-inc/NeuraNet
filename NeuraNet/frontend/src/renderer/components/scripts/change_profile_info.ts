
import axios from 'axios';
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as net from 'net';
import * as crypto from 'crypto';
import ConfigParser from 'configparser';
import * as receiver5 from '../../../main/receiver5';

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
  const RELAY_HOST = '34.28.13.79';
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
    const credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
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

export default function old_change_profile_info(first_name: string, last_name: string,
  username: any,
  email: string,
  password: string) {
  const RELAY_HOST = '34.28.13.79';
  const RELAY_PORT = 443;
  const senderSocket = new net.Socket();
  senderSocket.connect(RELAY_PORT, RELAY_HOST);

  receiver5.send_profile_info(senderSocket, first_name, last_name, username, email, password);
  return;
}

async function change_profile_info(first_name: string, last_name: string, username: any, email: string, password: string) {

  try {
    const response = await axios.get<{
      result: string;
      username: string;
      // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
    }>('https://website2-v3xlkt54dq-uc.a.run.app/change_profile/' + username + '/' + password + '/' + first_name + '/' + last_name + '/' + email + '/');
    // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');
    const result = response.data.result;
    if (result === 'success') {
      console.log("change profile success");
      return 'success';
    }
    if (result === 'fail') {
      console.log("change profilefailed");
      return 'failed';
    }
    if (result === 'user_already_exists') {
      console.log("user already exists");
      return 'exists';
    }

    else {
      console.log("change profilefailed");
      return 'change profile failed';
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}




function main(first_name: string, last_name: string, username: any, email: any, password: string): void {
}

export { main, change_profile_info };
