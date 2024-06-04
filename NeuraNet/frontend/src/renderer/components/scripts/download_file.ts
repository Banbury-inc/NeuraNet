
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


function download_file(files: string[], devices: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const RELAY_HOST = '0.0.0.0';
    const RELAY_PORT = 443;
    const senderSocket = new net.Socket();

    senderSocket.connect(RELAY_PORT, RELAY_HOST, () => {
      const null_arg = '';
      const file_header = `FILE_REQUEST:${files}:7679671:mmills6060:END_OF_HEADER`;
      senderSocket.write(file_header);
      // senderSocket.write("END_OF_HEADER");
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
          const file_name = splitHeader[1];
          const file_size = splitHeader[2];
          if (fileType === 'FILE_REQUEST') {

            console.log(`Device is requesting file: ${file_name}`);
            const directory_name: string = "BCloud";
            const directory_path: string = path.join(os.homedir(), directory_name);
            const file_save_path: string = path.join(directory_path, file_name);
            let request_file_name = path.basename(file_save_path);

            try {
              // Attempt to open the file
              const file: fs.ReadStream = fs.createReadStream(file_save_path);
              const null_string: string = "";
              const file_header: string = `FILE_REQUEST_RESPONSE:${request_file_name}:${file_size}:${null_string}:END_OF_HEADER`;
              senderSocket.write(file_header);

              let total_bytes_sent: number = 0;
              file.on('data', (bytes_read: Buffer) => {
                console.log("sending file...");
                senderSocket.write(bytes_read);
                total_bytes_sent += bytes_read.length;
              });

              file.on('end', () => {
                console.log(`${file_name} has been sent successfully.`);
                senderSocket.end();
              });

              file.on('error', (err: NodeJS.ErrnoException) => {
                console.error(`Error reading file: ${err}`);
                senderSocket.end();
              });

            } catch (error) {
              console.error(`Error sending file response: ${error}`);
              senderSocket.end();
            }


            resolve('received file request ;)');
          }
          if (fileType === 'REGISTRATION_FAILURE_USER_ALREADY_EXISTS') {
            resolve('exists');
          }
          else {
            resolve(fileType);
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

function main(files: string[], devices: string[]) {
  return download_file(files, devices);
}

export { main, download_file }
