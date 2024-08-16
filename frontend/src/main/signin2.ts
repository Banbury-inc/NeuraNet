
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as net from 'net';
import * as crypto from 'crypto';
import ConfigParser from 'configparser';
import { useState } from 'react';
import * as receiver from './receiver5';
import { ipcRenderer } from 'electron';




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
        const credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
        return JSON.parse(fs.readFileSync(credentialsFilePath, 'utf-8'));
    } catch (error) {
        return {};
    }
}

/**
 * Saves the credentials for a specific user, replacing any existing credentials in the file.
 *
 * @param {string} username - The username of the user logging in.
 * @param {string} passwordHash - The hashed password for the user.
 */
function saveCredentials(credentials: Record<string, string>): void {
    const config = new ConfigParser();
    config.read(CONFIG_FILE);
    const credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
    const credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);

    // Overwrite the existing credentials file with the new data
    fs.writeFileSync(credentialsFilePath, JSON.stringify(credentials, null, 4)); // Using null, 4 for pretty-printing
}

function deleteCredentialsFile(): void {
    const config = new ConfigParser();
    config.read(CONFIG_FILE);
    const credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
    const credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);

    fs.access(credentialsFilePath, fs.constants.F_OK, (err) => {
        if (err) {
            console.log('Credentials file does not exist:', credentialsFilePath);
        } else {
            fs.unlink(credentialsFilePath, (err) => {
                if (err) {
                    console.error('Failed to delete credentials file:', err);
                } else {
                    console.log('Credentials file successfully deleted:', credentialsFilePath);
                }
            });
        }
    });
}

function login(username: string, passwordStr: string): string {
    const senderSocket = connectToRelayServer();
    const endOfHeader = Buffer.from('END_OF_HEADER');
    let header: string | null = null;
    let buffer = Buffer.alloc(0);
    const fileHeader = `LOGIN_REQUEST::${passwordStr}:${username}:`;
    senderSocket.write(fileHeader);
    senderSocket.write(endOfHeader);

    let jobCompleted = false;
    while (!jobCompleted) {
        const data = senderSocket.read();
        if (!data) {
            break;
        }
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

        if (fileType === 'LOGIN_SUCCESS') {
            jobCompleted = true;
            const result = 'success';
            const hashedPassword = crypto.createHash('sha256').update(passwordStr).digest('hex');
            deleteCredentialsFile();
            // Create a new credentials object with only the current user's information
            const credentials = {
                username: hashedPassword
            };
            // Save the new credentials, replacing any existing ones
            saveCredentials(credentials);
            ipcRenderer.send('update-username', username);
            senderSocket.end();
            
            return result;
        } else if (fileType === 'LOGIN_FAIL') {
            jobCompleted = true;
            const result = 'fail';
            senderSocket.end();
            return result;
        }
    }
    senderSocket.end();
    return '';
}

function main(): void {
    if (process.argv.length > 3) {
        const username = process.argv[2];
        const passwordStr = process.argv[3];
        const result = login(username, passwordStr);

        console.log(`Result: ${result}`);
    } else {
        console.log('No argument received.');
    }
}

if (require.main === module) {
    main();
}
