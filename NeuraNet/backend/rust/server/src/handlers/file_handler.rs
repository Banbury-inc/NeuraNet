use super::database_handler;
use super::ping_handler;
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;

use mongodb::{
    bson::doc,
    sync::{Client, Collection},
};
use std::net::TcpStream;
pub fn process_file(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    let directory_name = "NeuraNet_File_Directory";
    let directory_path = format!(
        "{}/{}",
        std::env::current_dir().unwrap().to_str().unwrap(),
        directory_name
    );
    let file_path = format!("{}/{}", directory_name, _file_name);

    if !std::path::Path::new(&directory_path).exists() {
        println!("Directory does not exist, creating directory");
        std::fs::create_dir(&directory_path).unwrap();
    }

    println!("Receiving file...");

    // Write the buffer to the file
    let mut file = File::create(&file_path).unwrap();
    file.write_all(buffer.as_bytes()).unwrap();

    println!("File received and saved to {:?}", file_path);
}

pub fn process_file_request(
    buffer: &str,
    stream: &mut TcpStream,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) -> mongodb::error::Result<()> {
    println!("Received file request");
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;

    let collection: Collection<database_handler::Users> =
        client.database("myDatabase").collection("users");

    let cursor = collection.find(None, None)?;

    for result in cursor {
        let mut user = result?;
        let user_id = user._id.clone();
        let mut updated = false;

        // Iterate over devices and update their 'online' status if necessary
        for device in &mut user.devices {
            // search through each device, look to see if it is online
            if device.online {
                // if it is online, look to see if the file name exists in that device
                for file in &device.files {
                    if file.file_name == _file_name {
                        // if the file name exists, send a file request message to the device
                        // send the file request message to the device
                        let message = format!("FILE_REQUEST:{}:::END_OF_HEADER", _file_name);
                        let completed_send_message =
                            ping_handler::send_message(stream, &message).unwrap();

                        println!("sent file request to {}", device.device_name);
                    }
                }
            }
        }
    }

    Ok(())
}

pub fn process_file_request_response(
    buffer: &str,
    stream: &mut TcpStream,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file request response");
    let directory_name = "NeuraNet_File_Directory";
    let directory_path = format!(
        "{}/{}",
        std::env::current_dir().unwrap().to_str().unwrap(),
        directory_name
    );
    let file_path = format!("{}/{}", directory_name, _file_name);

    if !std::path::Path::new(&directory_path).exists() {
        println!("Directory does not exist, creating directory");
        std::fs::create_dir(&directory_path).unwrap();
    }
    println!("Receiving file...");

    // Write the buffer to the file
    let mut file = File::create(&file_path).unwrap();
    file.write_all(buffer.as_bytes()).unwrap();

    println!("File received and saved to {:?}", file_path);
}
pub fn process_file_delete_request(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file delete request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
pub fn process_file_delete_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file delete request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
