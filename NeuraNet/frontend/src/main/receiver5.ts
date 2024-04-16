import * as net from 'net';
import { config as dotenvConfig } from 'dotenv';
import * as subprocess from 'child_process';
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as util from 'util';
import si from '../../dependency/systeminformation'
import axios from 'axios';
import commander from 'commander';
import speedTest, { ResultEvent } from 'speedtest-net';
import { DateTime } from 'luxon';
import ConfigParser from 'configparser';


dotenvConfig();

interface FileHeader {
    file_type: string;
    file_name: string;
    file_size: number;
    username: string;
    password: string;
}

interface ProfileInfo {
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    password: string;
}

interface DeviceInfo {
    user: string;
    device_number: number;
    device_name: string;
    files: FileInfo[];
    storage_capacity_GB: number;
    date_added: string;
    ip_address: string;
    average_network_speed: number;
    upload_network_speed: number;
    download_network_speed: number;
    gpu_usage: number;
    cpu_usage: number;
    ram_usage: number;
    network_reliability: number;
    average_time_online: number;
    device_priority: number;
    sync_status: boolean;
    optimization_status: boolean;
}

interface SmallDeviceInfo {
    user: string;
    device_number: number;
    device_name: string;
    files: FileInfo[];
    date_added: string;
}


interface FileInfo {
    File_Name: string;
    Date_Uploaded: string;
    File_Size: number;
}


interface CPUPerformance {
    manufacturer: string;
    brand: string;
    speed: number;
    cores: number;
    physicalCores: number;
    processors: number;
}

interface GPUUsage {
    model: string;
    utilization: number;
    temperature: number;
}

interface memUsage {
    total: number;
    free: number;
    used: number;
    usagePercentage: number;
}

interface SpeedResult {
  upload: number;
  download: number;
}


interface IPAddress {
    networkInterfaces: string;
}


interface SpeedTestResult {
  download: number;
  upload: number;
  ping: number;
  downloadUnit: number;
  uploadUnit: number;
  pingUnit: string;
  server: {
    name: string;
    country: string;
    sponsor: string | undefined;
    id: number;
  };
}


async function run(receiver_socket: net.Socket): Promise<void> {
    const end_of_header = Buffer.from("END_OF_HEADER");
    let buffer: Buffer = Buffer.alloc(0);
    let header: FileHeader | null = null;

    receiver_socket.on('data', async (data: Buffer) => {
        buffer = Buffer.concat([buffer, data]);
        let index = buffer.indexOf(end_of_header);
        while (index !== -1) {
            const headerPart = buffer.slice(0, index);
            const content = buffer.slice(index + end_of_header.length);
            const headerStr = headerPart.toString();
            const [file_type, file_name, file_sizeStr, username, password] = headerStr.split(":");
            const file_size = parseInt(file_sizeStr, 10);

            header = {
                file_type,
                file_name,
                file_size,
                username,
                password
            };

            buffer = content;

            if (header.file_type === "MSG") {
                // Handle message
            } else if (header.file_type === "UPDATE") {
                // Handle update
            } else if (header.file_type === "FILE") {
                await handleFile(header, buffer);
            } else if (header.file_type === "FILE_REQUEST") {

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
                    receiver_socket.write(file_header);

                    let total_bytes_sent: number = 0;
                    file.on('data', (bytes_read: Buffer) => {
                        console.log("sending file...");
                        receiver_socket.write(bytes_read);
                        total_bytes_sent += bytes_read.length;
                    });

                    file.on('end', () => {
                        console.log(`${file_name} has been sent successfully.`);
                        receiver_socket.end();
                    });

                    file.on('error', (err: NodeJS.ErrnoException) => {
                        console.error(`Error reading file: ${err}`);
                        receiver_socket.end();
                    });

                } catch (error) {
                    console.error(`Error sending file response: ${error}`);
                    receiver_socket.end();
                }
            } else if (header.file_type === "FILE_REQUEST_RESPONSE") {
                console.log("Received file request response");
            } else if (header.file_type === "PING_REQUEST") {

              console.log("Received a ping request");
                // Handle ping request
              let credentials = loadCredentials();
              let user = Object.keys(credentials)[0];
              let device_number = 0
              let device_name = get_device_name();
              let files = get_directory_info();
              let storage_capacity_GB = await get_storage_capacity();
              let date_added = get_current_date_and_time();
              let ip_address = await get_ip_address();
              let average_network_speed = 0 
              let upload_network_speed = 0
              let download_network_speed = 0 
              let gpu_usage = await get_gpu_usage();
              let cpu_usage = await get_cpu_usage(); 
              let ram_usage = await get_ram_usage();
              let network_reliability = 0;
              let average_time_online = 0;
              let device_priority = 1;
              let sync_status = true;
              let optimization_status = true;
              
              const device_info_json: DeviceInfo = {
                  user,
                  device_number,
                  device_name,
                  files,
                  storage_capacity_GB,
                  date_added,
                  ip_address,
                  average_network_speed,
                  upload_network_speed,
                  download_network_speed,
                  gpu_usage,
                  cpu_usage,
                  ram_usage,
                  network_reliability,
                  average_time_online,
                  device_priority,
                  sync_status,
                  optimization_status
              };

              sendDeviceInfo(receiver_socket, device_info_json);

            } else if (header.file_type === "SMALL_PING_REQUEST") {


                // Handle ping request
              let credentials = loadCredentials();
              let user = Object.keys(credentials)[0];
              let device_number = 0
              let device_name = get_device_name();
              let files = get_directory_info();
              let date_added = get_current_date_and_time();
             
              const device_info_json: SmallDeviceInfo = {
                  user,
                  device_number,
                  device_name,
                  files,
                  date_added,
              };

              sendSmallDeviceInfo(receiver_socket, device_info_json);

            } else if (header.file_type === "FILE_DELETE_REQUEST") {
                // Handle file delete request
            } else {
                console.log("Unknown data type received");
            }

            index = buffer.indexOf(end_of_header);
        }
    });
}

async function handleFile(header: FileHeader, buffer: Buffer): Promise<void> {
    const directory_name = "BCloudReceiver";
    const directory_path = path.join(os.homedir(), directory_name);
    const file_save_path = path.join(directory_path, header.file_name);

    if (!fs.existsSync(directory_path)) {
        fs.mkdirSync(directory_path, { recursive: true });
        const welcome_file_path = path.join(directory_path, "welcome.txt");
        fs.writeFileSync(welcome_file_path, "Welcome to Banbury Cloud!");
    }

    const fileStream = fs.createWriteStream(file_save_path);
    fileStream.write(buffer);

    fileStream.on('error', (err) => {
        console.error("Error writing file:", err);
    });

    fileStream.on('close', () => {
        console.log(`Received ${header.file_name}.`);
    });
}


async function send_profile_info(sender_socket: net.Socket, first_name: string, last_name: string, username: string, email: string, password: string): Promise<void> {
    const get_current_date_and_time = (): string => {
        // Implement your logic to get current date and time
        return new Date().toISOString();
    };

    const date_time: string = get_current_date_and_time();
    const profile_info: Record<string, string> = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'password': password,
    };
    const profile_info_json: string = JSON.stringify(profile_info, null, 4);

    const null_string: string = "";
    const file_header: string = `CHANGE_PROFILE_REQUEST:${null_string}:${null_string}:${null_string}:END_OF_HEADER`;
    sender_socket.write(file_header);

    const profile_info_with_stop_signal: string = `${profile_info_json}END_OF_JSON`;
    sender_socket.write(profile_info_with_stop_signal);

    console.log(`${date_time} Ping response has been sent successfully.`);
  return;
}

async function sendDeviceInfo(sender_socket: net.Socket, device_info: DeviceInfo): Promise<void> {
    const date_time: string = get_current_date_and_time();
    const null_string: string = "";
    const file_header: string = `PING_REQUEST_RESPONSE:${null_string}:${null_string}:${null_string}:END_OF_HEADER`;
    sender_socket.write(file_header);

    const device_info_with_stop_signal: string = JSON.stringify(device_info) + "END_OF_JSON";
    sender_socket.write(device_info_with_stop_signal);
    console.log(device_info_with_stop_signal);
    console.log(`${date_time} Ping response has been sent successfully.`);
}

async function sendSmallDeviceInfo(sender_socket: net.Socket, device_info: SmallDeviceInfo): Promise<void> {
    const date_time: string = get_current_date_and_time();
    const null_string: string = "";
    const file_header: string = `SMALL_PING_REQUEST_RESPONSE:${null_string}:${null_string}:${null_string}:END_OF_HEADER`;
    sender_socket.write(file_header);

    const device_info_with_stop_signal: string = JSON.stringify(device_info) + "END_OF_JSON";
    sender_socket.write(device_info_with_stop_signal);
}

async function get_cpu_info(): Promise<CPUPerformance> {
    try {
        const cpuData = await si.cpu();
        const cpuPerformance: CPUPerformance = {
            manufacturer: cpuData.manufacturer || 'Unknown',
            brand: cpuData.brand || 'Unknown',
            speed: cpuData.speed || 0,
            cores: cpuData.cores || 0,
            physicalCores: cpuData.physicalCores || 0,
            processors: cpuData.processors || 0
        };
        return cpuPerformance;
    } catch (error) {
        console.error('Error retrieving CPU performance:', error);
        throw error; // Rethrow error to handle externally
    }
}

async function get_cpu_usage(): Promise<number> {
    try {
        const cpuData = await si.currentLoad();
        const cpuUsage = cpuData.currentLoad || 0;
        return cpuUsage;
    } catch (error) {
        console.error('Error retrieving CPU usage:', error);
        throw error; // Rethrow error to handle externally
    }
}

async function get_gpu_usage(): Promise<number> {
    try {
        const gpuData = await si.graphics();
        const totalUtilization = gpuData.controllers.reduce((total, controller) => total + (controller.utilizationGpu || 0), 0);
        return totalUtilization / gpuData.controllers.length;
    } catch (error) {
        console.error('Error retrieving GPU utilization:', error);
        throw error; // Rethrow error to handle externally
    }
}

async function get_ram_usage(): Promise<number> {
    try {
        const memData = await si.mem();
        const totalMemory = memData.total || 0;
        const usedMemory = memData.used || 0;
        const freeMemory = memData.free || 0;
        
        const usagePercentage = (usedMemory / totalMemory) * 100;

        const ramUsage: memUsage = {
            total: totalMemory,
            free: freeMemory,
            used: usedMemory,
            usagePercentage: isNaN(usagePercentage) ? 0 : usagePercentage // Handle NaN case
        };
        
       return isNaN(usagePercentage) ? 0 : usagePercentage; // Handle NaN case
    } catch (error) {
        console.error('Error retrieving RAM usage:', error);
        throw error; // Rethrow error to handle externally
    }
}

async function get_storage_capacity(): Promise<number> {
    try {
        const diskData = await si.fsSize();
        const totalCapacityBytes = diskData.reduce((total, disk) => total + disk.size, 0);
        const totalCapacityGB = totalCapacityBytes / (1024 * 1024 * 1024); // Convert bytes to GB
        return totalCapacityGB;
        } catch (error) {
        console.error('Error retrieving storage capacity:', error);
        throw error; // Rethrow error to handle externally
    }
}

async function get_ip_address(): Promise<string> {
    let ip_address: string | null = null;

    try {
        const response = await axios.get('https://httpbin.org/ip');
        const ip_info = response.data;
        const origin: string = ip_info.origin || 'Unknown';
        ip_address = origin.split(',')[0];
    } catch (error) {
        console.error('Error occurred:', error);
        ip_address = 'Unknown';
    }

    return ip_address || 'Unknown';
}


function get_current_date_and_time(): string {
    const now: Date = new Date();
    const year: number = now.getFullYear();
    const month: number = now.getMonth() + 1; // Month is zero-based, so we add 1
    const day: number = now.getDate();
    const hours: number = now.getHours();
    const minutes: number = now.getMinutes();
    const seconds: number = now.getSeconds();

    // Format the date and time
    const formattedDateTime: string = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')} ${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    return formattedDateTime;
}


function get_device_name(): string {
    return os.hostname();
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

function get_directory_info() {
    const directoryName = "BCloud"
    const directoryPath = os.homedir() + `/${directoryName}`;
    const filesInfo: any[] = [];

    // Check if the directory exists, create if it does not and create a welcome text file
    if (!fs.existsSync(directoryPath)) {
        fs.mkdirSync(directoryPath, { recursive: true });
        const welcomeFilePath = directoryPath + "/welcome.txt";
        fs.writeFileSync(welcomeFilePath,
            "Welcome to Banbury Cloud! This is the directory that will contain all of the files " +
            "that you would like to have in the cloud and streamed throughout all of your devices. " +
            "You may place as many files in here as you would like, and they will appear on all of " +
            "your other devices."
        );
    }

    // Loop through each file in the directory
    const files = fs.readdirSync(directoryPath);
    for (const filename of files) {
        const filePath = directoryPath + '/' + filename;

        // Skip directories, only process files
        if (fs.statSync(filePath).isFile()) {
            // Get file stats
            const stats = fs.statSync(filePath);
            const fileInfo = {
                "File Name": filename,
                "Date Uploaded": DateTime.fromMillis(stats.mtimeMs).toFormat('yyyy-MM-dd HH:mm:ss'),
                "File Size": stats.size
            };
            filesInfo.push(fileInfo);
        }
    }

    return filesInfo;
}


async function main(): Promise<void> {
    const SERVER_HOST = '34.28.13.79'
    const SERVER_PORT = 443;
    const receiver_socket = new net.Socket();

    receiver_socket.connect(SERVER_PORT, SERVER_HOST, () => {
        console.log("Connected to server");
    });

    receiver_socket.on('error', (err) => {
        console.error("Error:", err);
    });
    run(receiver_socket);
}

main();

export { get_cpu_info, get_cpu_usage, get_gpu_usage, get_ram_usage, get_storage_capacity, get_ip_address, get_current_date_and_time, get_device_name, loadCredentials, get_directory_info, run, handleFile, send_profile_info, sendDeviceInfo, sendSmallDeviceInfo, CPUPerformance, GPUUsage, memUsage, ProfileInfo, DeviceInfo, SmallDeviceInfo, FileInfo, FileHeader, SpeedResult, IPAddress, SpeedTestResult };
