
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

async function register(first_name: string, last_name: string, username: string, password_str: string) {

  try {
    const response = await axios.get<{
      result: string;
      username: string;
      // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo2/' + username + '/');
    }>('https://website2-v3xlkt54dq-uc.a.run.app/register/' + username + '/' + password_str + '/' + first_name + '/' + last_name + '/');
    // }>('https://website2-v3xlkt54dq-uc.a.run.app/getuserinfo/');
    const result = response.data.result;
    if (result === 'success') {
      console.log("register success");
      return 'success';
    }
    if (result === 'fail') {
      console.log("register failed");
      return 'failed';
    }
    if (result === 'user_already_exists') {
      console.log("user already exists");
      return 'exists';
    }

    else {
      console.log("register failed");
      return 'register failed';
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}


function register1(first_name: string, last_name: string, username: string, password_str: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const RELAY_HOST = '34.28.13.79';
    const RELAY_PORT = 443;
    const senderSocket = new net.Socket();

    senderSocket.connect(RELAY_PORT, RELAY_HOST, () => {
      const null_arg = '';
      const file_header = `REGISTRATION_REQUEST:${null_arg}:${password_str}:${username}:`;
      senderSocket.write(file_header);
      senderSocket.write("END_OF_HEADER");
      const user_info = {
        "username": username,
        "password": password_str,
        "first_name": first_name,
        "last_name": last_name
      };
      const user_info_json = JSON.stringify(user_info);
      const user_info_with_stop_signal: string = `${user_info_json}END_OF_JSON`;
      senderSocket.write(user_info_with_stop_signal);
    });

    const endOfHeader = Buffer.from('END_OF_HEADER');
    let buffer = Buffer.alloc(0);

    senderSocket.on('data', (data) => {
      buffer = Buffer.concat([buffer, data]);
      if (buffer.includes(endOfHeader)) {
        const endOfHeaderIndex = buffer.indexOf(endOfHeader);
        if (endOfHeaderIndex !== -1) {
          const headerPart = buffer.slice(0, endOfHeaderIndex);
          const content = buffer.slice(endOfHeaderIndex + endOfHeader.length);
          buffer = content;  // Update buffer to remove processed header

          const header = headerPart.toString();
          const splitHeader = header.split(':');
          const fileType = splitHeader[0];

          if (fileType === 'REGISTRATION_SUCCESS') {
            resolve('success');
          }
          if (fileType === 'REGISTRATION_FAILURE_USER_ALREADY_EXISTS') {
            resolve('exists');
          }

        }
      }
    });

    senderSocket.on('end', () => {
      console.log('Disconnected from server');
      reject(new Error('Connection ended without confirmation'));
    });

    senderSocket.on('error', (err) => {
      console.error('Socket error:', err);
      reject(err);
    });

    senderSocket.on('close', hadError => {
      if (!hadError) {
        reject(new Error('Connection closed unexpectedly'));
      }
    });
  });
}

function main(firstName: string, lastName: string, username: string, password: string) {
  return register(firstName, lastName, username, password);
}

export { main, register }
