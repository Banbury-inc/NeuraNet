"use strict";
exports.__esModule = true;
var os = require("os");
var fs = require("fs");
var path = require("path");
var dotenv = require("dotenv");
var net = require("net");
var crypto = require("crypto");
var configparser_1 = require("configparser");
var electron_1 = require("electron");
dotenv.config();
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
function connectToRelayServer() {
    // const RELAY_HOST = '34.28.13.79';
    var RELAY_HOST = '0.0.0.0';
    var RELAY_PORT = 443;
    var senderSocket = new net.Socket();
    senderSocket.connect(RELAY_PORT, RELAY_HOST);
    return senderSocket;
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
/**
 * Saves the credentials for a specific user, replacing any existing credentials in the file.
 *
 * @param {string} username - The username of the user logging in.
 * @param {string} passwordHash - The hashed password for the user.
 */
function saveCredentials(credentials) {
    var config = new configparser_1["default"]();
    config.read(CONFIG_FILE);
    var credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
    var credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
    // Overwrite the existing credentials file with the new data
    fs.writeFileSync(credentialsFilePath, JSON.stringify(credentials, null, 4)); // Using null, 4 for pretty-printing
}
function deleteCredentialsFile() {
    var config = new configparser_1["default"]();
    config.read(CONFIG_FILE);
    var credentialsFile = config.get('banbury_cloud', 'credentials_file') || 'default_filename.json';
    var credentialsFilePath = path.join(BANBURY_FOLDER, credentialsFile);
    fs.access(credentialsFilePath, fs.constants.F_OK, function (err) {
        if (err) {
            console.log('Credentials file does not exist:', credentialsFilePath);
        }
        else {
            fs.unlink(credentialsFilePath, function (err) {
                if (err) {
                    console.error('Failed to delete credentials file:', err);
                }
                else {
                    console.log('Credentials file successfully deleted:', credentialsFilePath);
                }
            });
        }
    });
}
function login(username, passwordStr) {
    var senderSocket = connectToRelayServer();
    var endOfHeader = Buffer.from('END_OF_HEADER');
    var header = null;
    var buffer = Buffer.alloc(0);
    var fileHeader = "LOGIN_REQUEST::".concat(passwordStr, ":").concat(username, ":");
    senderSocket.write(fileHeader);
    senderSocket.write(endOfHeader);
    var jobCompleted = false;
    while (!jobCompleted) {
        var data = senderSocket.read();
        if (!data) {
            break;
        }
        buffer = Buffer.concat([buffer, data]);
        var fileType = 'Unknown';
        if (buffer.includes(endOfHeader) && !header) {
            var endOfHeaderIndex = buffer.indexOf(endOfHeader);
            if (endOfHeaderIndex !== -1) {
                var headerPart = buffer.slice(0, endOfHeaderIndex);
                var content = buffer.slice(endOfHeaderIndex + endOfHeader.length);
                header = headerPart.toString();
                var splitHeader = header.split(':');
                fileType = splitHeader[0];
                buffer = content;
            }
        }
        if (fileType === 'LOGIN_SUCCESS') {
            jobCompleted = true;
            var result = 'success';
            var hashedPassword = crypto.createHash('sha256').update(passwordStr).digest('hex');
            deleteCredentialsFile();
            // Create a new credentials object with only the current user's information
            var credentials = {
                username: hashedPassword
            };
            // Save the new credentials, replacing any existing ones
            saveCredentials(credentials);
            electron_1.ipcRenderer.send('update-username', username);
            senderSocket.end();
            return result;
        }
        else if (fileType === 'LOGIN_FAIL') {
            jobCompleted = true;
            var result = 'fail';
            senderSocket.end();
            return result;
        }
    }
    senderSocket.end();
    return '';
}
function main() {
    if (process.argv.length > 3) {
        var username = process.argv[2];
        var passwordStr = process.argv[3];
        var result = login(username, passwordStr);
        console.log("Result: ".concat(result));
    }
    else {
        console.log('No argument received.');
    }
}
if (require.main === module) {
    main();
}
