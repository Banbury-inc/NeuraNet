
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as net from 'net';
import * as crypto from 'crypto';
import ConfigParser from 'configparser';

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

function delete_file(device_name: string[]): string {
    const senderSocket = connectToRelayServer();
    const endOfHeader = Buffer.from('END_OF_HEADER');
    const credentials = loadCredentials();
    let username = Object.keys(credentials)[0];
    const file_size = ""
    let header: string | null = null;
    let buffer = Buffer.alloc(0);
    let null_arg = ""
    const fileHeader = `DEVICE_DELETE_REQUEST:${device_name}:${null_arg}:${username}:`;
    senderSocket.write(fileHeader);
    senderSocket.write(endOfHeader);

    let jobCompleted = false;
    senderSocket.on('data', (data) => {
        buffer = Buffer.concat([buffer, data]);
        let fileType = 'Unknown';
        if (buffer.includes(endOfHeader) && !header) {
            const endOfHeaderIndex = buffer.indexOf(endOfHeader);
            if (endOfHeaderIndex !== -1) {
                const headerPart = buffer.slice(0, endOfHeaderIndex);
                const content = buffer.slice(endOfHeaderIndex + endOfHeader.length);
                header = headerPart.toString();
                const splitHeader = header.split(':');
                fileType = splitHeader[0];
                buffer = content;
            }
        }
    });

    senderSocket.on('end', () => {
        if (!jobCompleted) {
            console.log('Connection closed before login completion.');
        }
    });

    senderSocket.on('error', (err) => {
        console.error('Error during login:', err);
        senderSocket.end();
    });

    return '';
}


function main(device_name: string[]): void {
      const result = delete_file(device_name);
    }

export default main;
