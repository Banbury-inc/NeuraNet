"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.sendSmallDeviceInfo = exports.sendDeviceInfo = exports.send_profile_info = exports.handleFile = exports.run = exports.get_directory_info = exports.loadCredentials = exports.get_device_name = exports.get_current_date_and_time = exports.get_ip_address = exports.get_storage_capacity = exports.get_ram_usage = exports.get_gpu_usage = exports.get_cpu_usage = exports.get_cpu_info = void 0;
var dotenv_1 = require("dotenv");
var os = require("os");
var fs = require("fs");
var path = require("path");
var systeminformation_1 = require("../../dependency/systeminformation");
var axios_1 = require("axios");
var luxon_1 = require("luxon");
var configparser_1 = require("configparser");
var AuthContext_1 = require("../renderer/context/AuthContext");
(0, dotenv_1.config)();
function run(receiver_socket, global_username) {
    return __awaiter(this, void 0, void 0, function () {
        var end_of_header, buffer, header;
        var _this = this;
        return __generator(this, function (_a) {
            console.log("receiver running");
            end_of_header = Buffer.from("END_OF_HEADER");
            buffer = Buffer.alloc(0);
            header = null;
            receiver_socket.on('data', function (data) { return __awaiter(_this, void 0, void 0, function () {
                var index, _loop_1;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            buffer = Buffer.concat([buffer, data]);
                            console.log(buffer);
                            index = buffer.indexOf(end_of_header);
                            _loop_1 = function () {
                                var headerPart, content, headerStr, _b, file_type, file_name, file_sizeStr, username, password, file_size, directory_name, directory_path, file_save_path, request_file_name, file, null_string, file_header, total_bytes_sent_1, credentials, user, device_number, device_name, files, storage_capacity_GB, max_storage_capacity_GB, date_added, ip_address, average_network_speed, upload_network_speed, download_network_speed, gpu_usage, cpu_usage, ram_usage, predicted_upload_network_speed, predicted_download_network_speed, predicted_gpu_usage, predicted_cpu_usage, predicted_ram_usage, predicted_performance_score, network_reliability, average_time_online, tasks, device_priority, sync_status, optimization_status, online, device_info_json, credentials, user, device_number, device_name, files, date_added, device_info_json;
                                return __generator(this, function (_c) {
                                    switch (_c.label) {
                                        case 0:
                                            headerPart = buffer.slice(0, index);
                                            content = buffer.slice(index + end_of_header.length);
                                            headerStr = headerPart.toString();
                                            _b = headerStr.split(":"), file_type = _b[0], file_name = _b[1], file_sizeStr = _b[2], username = _b[3], password = _b[4];
                                            file_size = parseInt(file_sizeStr, 10);
                                            header = {
                                                file_type: file_type,
                                                file_name: file_name,
                                                file_size: file_size,
                                                username: username,
                                                password: password
                                            };
                                            buffer = content;
                                            if (!(header.file_type === "MSG")) return [3 /*break*/, 1];
                                            return [3 /*break*/, 13];
                                        case 1:
                                            if (!(header.file_type === "UPDATE")) return [3 /*break*/, 2];
                                            return [3 /*break*/, 13];
                                        case 2:
                                            if (!(header.file_type === "FILE")) return [3 /*break*/, 4];
                                            return [4 /*yield*/, handleFile(header, buffer)];
                                        case 3:
                                            _c.sent();
                                            return [3 /*break*/, 13];
                                        case 4:
                                            if (!(header.file_type === "FILE_REQUEST")) return [3 /*break*/, 5];
                                            console.log("Device is requesting file: ".concat(file_name));
                                            directory_name = "BCloud";
                                            directory_path = path.join(os.homedir(), directory_name);
                                            file_save_path = path.join(directory_path, file_name);
                                            request_file_name = path.basename(file_save_path);
                                            try {
                                                file = fs.createReadStream(file_save_path);
                                                null_string = "";
                                                file_header = "FILE_REQUEST_RESPONSE:".concat(request_file_name, ":").concat(file_size, ":").concat(null_string, ":END_OF_HEADER");
                                                receiver_socket.write(file_header);
                                                total_bytes_sent_1 = 0;
                                                file.on('data', function (bytes_read) {
                                                    console.log("sending file...");
                                                    receiver_socket.write(bytes_read);
                                                    total_bytes_sent_1 += bytes_read.length;
                                                });
                                                file.on('end', function () {
                                                    console.log("".concat(file_name, " has been sent successfully."));
                                                    receiver_socket.end();
                                                });
                                                file.on('error', function (err) {
                                                    console.error("Error reading file: ".concat(err));
                                                    receiver_socket.end();
                                                });
                                            }
                                            catch (error) {
                                                console.error("Error sending file response: ".concat(error));
                                                receiver_socket.end();
                                            }
                                            return [3 /*break*/, 13];
                                        case 5:
                                            if (!(header.file_type === "FILE_REQUEST_RESPONSE")) return [3 /*break*/, 6];
                                            console.log("Received file request response");
                                            return [3 /*break*/, 13];
                                        case 6:
                                            if (!(header.file_type === "PING_REQUEST")) return [3 /*break*/, 12];
                                            console.log("Received a ping request");
                                            credentials = loadCredentials();
                                            user = global_username;
                                            device_number = 0;
                                            device_name = get_device_name();
                                            files = get_directory_info();
                                            return [4 /*yield*/, get_storage_capacity()];
                                        case 7:
                                            storage_capacity_GB = _c.sent();
                                            max_storage_capacity_GB = 50;
                                            date_added = get_current_date_and_time();
                                            return [4 /*yield*/, get_ip_address()];
                                        case 8:
                                            ip_address = _c.sent();
                                            average_network_speed = 0;
                                            upload_network_speed = 0;
                                            download_network_speed = 0;
                                            return [4 /*yield*/, get_gpu_usage()];
                                        case 9:
                                            gpu_usage = _c.sent();
                                            return [4 /*yield*/, get_cpu_usage()];
                                        case 10:
                                            cpu_usage = _c.sent();
                                            return [4 /*yield*/, get_ram_usage()];
                                        case 11:
                                            ram_usage = _c.sent();
                                            predicted_upload_network_speed = 0;
                                            predicted_download_network_speed = 0;
                                            predicted_gpu_usage = 0;
                                            predicted_cpu_usage = 0;
                                            predicted_ram_usage = 0;
                                            predicted_performance_score = 0;
                                            network_reliability = 0;
                                            average_time_online = 0;
                                            tasks = 0;
                                            device_priority = 1;
                                            sync_status = true;
                                            optimization_status = true;
                                            online = true;
                                            device_info_json = {
                                                user: user,
                                                device_number: device_number,
                                                device_name: device_name,
                                                files: files,
                                                storage_capacity_GB: storage_capacity_GB,
                                                max_storage_capacity_GB: max_storage_capacity_GB,
                                                date_added: date_added,
                                                ip_address: ip_address,
                                                average_network_speed: average_network_speed,
                                                upload_network_speed: upload_network_speed,
                                                download_network_speed: download_network_speed,
                                                gpu_usage: gpu_usage,
                                                cpu_usage: cpu_usage,
                                                ram_usage: ram_usage,
                                                predicted_upload_network_speed: predicted_upload_network_speed,
                                                predicted_download_network_speed: predicted_download_network_speed,
                                                predicted_gpu_usage: predicted_gpu_usage,
                                                predicted_cpu_usage: predicted_cpu_usage,
                                                predicted_ram_usage: predicted_ram_usage,
                                                predicted_performance_score: predicted_performance_score,
                                                network_reliability: network_reliability,
                                                average_time_online: average_time_online,
                                                tasks: tasks,
                                                device_priority: device_priority,
                                                sync_status: sync_status,
                                                optimization_status: optimization_status,
                                                online: online
                                            };
                                            sendDeviceInfo(receiver_socket, device_info_json);
                                            return [3 /*break*/, 13];
                                        case 12:
                                            if (header.file_type === "SMALL_PING_REQUEST") {
                                                console.log("received small ping request");
                                                credentials = loadCredentials();
                                                user = global_username;
                                                device_number = 0;
                                                device_name = get_device_name();
                                                files = get_directory_info();
                                                date_added = get_current_date_and_time();
                                                device_info_json = {
                                                    user: user,
                                                    device_number: device_number,
                                                    device_name: device_name,
                                                    files: files,
                                                    date_added: date_added
                                                };
                                                sendSmallDeviceInfo(receiver_socket, device_info_json);
                                                console.log("completed smal ping request");
                                            }
                                            else if (header.file_type === "FILE_DELETE_REQUEST") {
                                                // Handle file delete request
                                            }
                                            else {
                                                console.log("Unknown data type received");
                                            }
                                            _c.label = 13;
                                        case 13:
                                            index = buffer.indexOf(end_of_header);
                                            return [2 /*return*/];
                                    }
                                });
                            };
                            _a.label = 1;
                        case 1:
                            if (!(index !== -1)) return [3 /*break*/, 3];
                            return [5 /*yield**/, _loop_1()];
                        case 2:
                            _a.sent();
                            return [3 /*break*/, 1];
                        case 3: return [2 /*return*/];
                    }
                });
            }); });
            return [2 /*return*/];
        });
    });
}
exports.run = run;
function handleFile(header, buffer) {
    return __awaiter(this, void 0, void 0, function () {
        var directory_name, directory_path, file_save_path, welcome_file_path, fileStream;
        return __generator(this, function (_a) {
            directory_name = "BCloudReceiver";
            directory_path = path.join(os.homedir(), directory_name);
            file_save_path = path.join(directory_path, header.file_name);
            if (!fs.existsSync(directory_path)) {
                fs.mkdirSync(directory_path, { recursive: true });
                welcome_file_path = path.join(directory_path, "welcome.txt");
                fs.writeFileSync(welcome_file_path, "Welcome to Banbury Cloud!");
            }
            fileStream = fs.createWriteStream(file_save_path);
            fileStream.write(buffer);
            fileStream.on('error', function (err) {
                console.error("Error writing file:", err);
            });
            fileStream.on('close', function () {
                console.log("Received ".concat(header.file_name, "."));
            });
            return [2 /*return*/];
        });
    });
}
exports.handleFile = handleFile;
function send_profile_info(sender_socket, first_name, last_name, username, email, password) {
    return __awaiter(this, void 0, void 0, function () {
        var get_current_date_and_time, date_time, profile_info, profile_info_json, null_string, file_header, profile_info_with_stop_signal;
        return __generator(this, function (_a) {
            get_current_date_and_time = function () {
                // Implement your logic to get current date and time
                return new Date().toISOString();
            };
            date_time = get_current_date_and_time();
            profile_info = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': password
            };
            profile_info_json = JSON.stringify(profile_info, null, 4);
            null_string = "";
            file_header = "CHANGE_PROFILE_REQUEST:".concat(null_string, ":").concat(null_string, ":").concat(null_string, ":END_OF_HEADER");
            sender_socket.write(file_header);
            profile_info_with_stop_signal = "".concat(profile_info_json, "END_OF_JSON");
            sender_socket.write(profile_info_with_stop_signal);
            console.log("".concat(date_time, " Ping response has been sent successfully."));
            return [2 /*return*/];
        });
    });
}
exports.send_profile_info = send_profile_info;
function sendDeviceInfo(sender_socket, device_info) {
    return __awaiter(this, void 0, void 0, function () {
        var date_time, null_string, file_header, device_info_with_stop_signal;
        return __generator(this, function (_a) {
            date_time = get_current_date_and_time();
            null_string = "";
            file_header = "PING_REQUEST_RESPONSE:".concat(null_string, ":").concat(null_string, ":").concat(null_string, ":END_OF_HEADER");
            sender_socket.write(file_header);
            device_info_with_stop_signal = JSON.stringify(device_info) + "END_OF_JSON";
            sender_socket.write(device_info_with_stop_signal);
            console.log(device_info_with_stop_signal);
            console.log("".concat(date_time, " Ping response has been sent successfully."));
            return [2 /*return*/];
        });
    });
}
exports.sendDeviceInfo = sendDeviceInfo;
function sendSmallDeviceInfo(sender_socket, device_info) {
    return __awaiter(this, void 0, void 0, function () {
        var date_time, null_string, file_header, device_info_with_stop_signal;
        return __generator(this, function (_a) {
            date_time = get_current_date_and_time();
            null_string = "";
            file_header = "SMALL_PING_REQUEST_RESPONSE:".concat(null_string, ":").concat(null_string, ":").concat(null_string, ":END_OF_HEADER");
            sender_socket.write(file_header);
            device_info_with_stop_signal = JSON.stringify(device_info) + "END_OF_JSON";
            sender_socket.write(device_info_with_stop_signal);
            return [2 /*return*/];
        });
    });
}
exports.sendSmallDeviceInfo = sendSmallDeviceInfo;
function get_cpu_info() {
    return __awaiter(this, void 0, void 0, function () {
        var cpuData, cpuPerformance, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, systeminformation_1["default"].cpu()];
                case 1:
                    cpuData = _a.sent();
                    cpuPerformance = {
                        manufacturer: cpuData.manufacturer || 'Unknown',
                        brand: cpuData.brand || 'Unknown',
                        speed: cpuData.speed || 0,
                        cores: cpuData.cores || 0,
                        physicalCores: cpuData.physicalCores || 0,
                        processors: cpuData.processors || 0
                    };
                    return [2 /*return*/, cpuPerformance];
                case 2:
                    error_1 = _a.sent();
                    console.error('Error retrieving CPU performance:', error_1);
                    throw error_1; // Rethrow error to handle externally
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.get_cpu_info = get_cpu_info;
function get_cpu_usage() {
    return __awaiter(this, void 0, void 0, function () {
        var cpuData, cpuUsage, error_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, systeminformation_1["default"].currentLoad()];
                case 1:
                    cpuData = _a.sent();
                    cpuUsage = cpuData.currentLoad || 0;
                    return [2 /*return*/, cpuUsage];
                case 2:
                    error_2 = _a.sent();
                    console.error('Error retrieving CPU usage:', error_2);
                    throw error_2; // Rethrow error to handle externally
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.get_cpu_usage = get_cpu_usage;
function get_gpu_usage() {
    return __awaiter(this, void 0, void 0, function () {
        var gpuData, totalUtilization, error_3;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, systeminformation_1["default"].graphics()];
                case 1:
                    gpuData = _a.sent();
                    totalUtilization = gpuData.controllers.reduce(function (total, controller) { return total + (controller.utilizationGpu || 0); }, 0);
                    return [2 /*return*/, totalUtilization / gpuData.controllers.length];
                case 2:
                    error_3 = _a.sent();
                    console.error('Error retrieving GPU utilization:', error_3);
                    throw error_3; // Rethrow error to handle externally
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.get_gpu_usage = get_gpu_usage;
function get_ram_usage() {
    return __awaiter(this, void 0, void 0, function () {
        var memData, totalMemory, usedMemory, freeMemory, usagePercentage, ramUsage, error_4;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, systeminformation_1["default"].mem()];
                case 1:
                    memData = _a.sent();
                    totalMemory = memData.total || 0;
                    usedMemory = memData.used || 0;
                    freeMemory = memData.free || 0;
                    usagePercentage = (usedMemory / totalMemory) * 100;
                    ramUsage = {
                        total: totalMemory,
                        free: freeMemory,
                        used: usedMemory,
                        usagePercentage: isNaN(usagePercentage) ? 0 : usagePercentage // Handle NaN case
                    };
                    return [2 /*return*/, isNaN(usagePercentage) ? 0 : usagePercentage]; // Handle NaN case
                case 2:
                    error_4 = _a.sent();
                    console.error('Error retrieving RAM usage:', error_4);
                    throw error_4; // Rethrow error to handle externally
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.get_ram_usage = get_ram_usage;
function get_storage_capacity() {
    return __awaiter(this, void 0, void 0, function () {
        var diskData, totalCapacityBytes, totalCapacityGB, error_5;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, systeminformation_1["default"].fsSize()];
                case 1:
                    diskData = _a.sent();
                    totalCapacityBytes = diskData.reduce(function (total, disk) { return total + disk.size; }, 0);
                    totalCapacityGB = totalCapacityBytes / (1024 * 1024 * 1024);
                    return [2 /*return*/, totalCapacityGB];
                case 2:
                    error_5 = _a.sent();
                    console.error('Error retrieving storage capacity:', error_5);
                    throw error_5; // Rethrow error to handle externally
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.get_storage_capacity = get_storage_capacity;
function get_ip_address() {
    return __awaiter(this, void 0, void 0, function () {
        var ip_address, response, ip_info, origin_1, error_6;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    ip_address = null;
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, axios_1["default"].get('https://httpbin.org/ip')];
                case 2:
                    response = _a.sent();
                    ip_info = response.data;
                    origin_1 = ip_info.origin || 'Unknown';
                    ip_address = origin_1.split(',')[0];
                    return [3 /*break*/, 4];
                case 3:
                    error_6 = _a.sent();
                    console.error('Error occurred:', error_6);
                    ip_address = 'Unknown';
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/, ip_address || 'Unknown'];
            }
        });
    });
}
exports.get_ip_address = get_ip_address;
function get_current_date_and_time() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1; // Month is zero-based, so we add 1
    var day = now.getDate();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    // Format the date and time
    var formattedDateTime = "".concat(year, "-").concat(month.toString().padStart(2, '0'), "-").concat(day.toString().padStart(2, '0'), " ").concat(hours.toString().padStart(2, '0'), ":").concat(minutes.toString().padStart(2, '0'), ":").concat(seconds.toString().padStart(2, '0'));
    return formattedDateTime;
}
exports.get_current_date_and_time = get_current_date_and_time;
function get_device_name() {
    return os.hostname();
}
exports.get_device_name = get_device_name;
function get_username() {
    var username = (0, AuthContext_1.useAuth)().username;
    return username;
}
function loadCredentials() {
    try {
        var config = new configparser_1["default"]();
        config.read(CONFIG_FILE);
        var credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
        var credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
        return JSON.parse(fs.readFileSync(credentialsFilePath, 'utf-8'));
    }
    catch (error) {
        return {};
    }
}
exports.loadCredentials = loadCredentials;
var homeDirectory = os.homedir();
var BANBURY_FOLDER = path.join(homeDirectory, '.banbury');
var CONFIG_FILE = path.join(BANBURY_FOLDER, '.banbury_config.ini');
if (!fs.existsSync(BANBURY_FOLDER)) {
    fs.mkdirSync(BANBURY_FOLDER);
}
if (!fs.existsSync(CONFIG_FILE)) {
    var config = new configparser_1["default"]();
    config.set('banbury_cloud', 'credentials_file', 'credentials.json');
    fs.writeFileSync(CONFIG_FILE, config.toString());
}
function get_directory_info() {
    var directoryName = "BCloud";
    var directoryPath = os.homedir() + "/".concat(directoryName);
    var filesInfo = [];
    // Check if the directory exists, create if it does not and create a welcome text file
    if (!fs.existsSync(directoryPath)) {
        fs.mkdirSync(directoryPath, { recursive: true });
        var welcomeFilePath = directoryPath + "/welcome.txt";
        fs.writeFileSync(welcomeFilePath, "Welcome to Banbury Cloud! This is the directory that will contain all of the files " +
            "that you would like to have in the cloud and streamed throughout all of your devices. " +
            "You may place as many files in here as you would like, and they will appear on all of " +
            "your other devices.");
    }
    // Loop through each file in the directory
    var files = fs.readdirSync(directoryPath);
    for (var _i = 0, files_1 = files; _i < files_1.length; _i++) {
        var filename = files_1[_i];
        var filePath = directoryPath + '/' + filename;
        // Skip directories, only process files
        if (fs.statSync(filePath).isFile()) {
            // Get file stats
            var stats = fs.statSync(filePath);
            var fileInfo = {
                "File Name": filename,
                "Date Uploaded": luxon_1.DateTime.fromMillis(stats.mtimeMs).toFormat('yyyy-MM-dd HH:mm:ss'),
                "File Size": stats.size,
                "File Priority": 5,
                "Original_Device": filename
            };
            filesInfo.push(fileInfo);
        }
    }
    return filesInfo;
}
exports.get_directory_info = get_directory_info;
