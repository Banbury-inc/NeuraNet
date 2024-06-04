use super::database_handler;
use super::database_handler::Users;
use super::ping_handler;
use super::ping_handler::send_message;
use mongodb::{
    bson::doc,
    sync::{Client, Collection},
};
use std::fs::{self, File};
use std::io::{self, Read, Write};
use std::net::TcpStream;
use std::path::Path;
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
    _buffer: &str,
    stream: &mut TcpStream,
    file_name: &str,
    file_size: &str,
    username: &str,
) -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");
    println!("Received file request");

    let user = database_handler::get_user(username).unwrap();
    // println!("User: {:?}", user);
    let mut message = format!("FILE_REQUEST:{}:{}:END_OF_HEADER", file_name, file_size);
    // check if the user exists
    if user.is_none() {
        println!("User does not exist");
        send_message(stream, "LOGIN_FAIL:");
        return Ok(());
    } else {
        println!("sending file request :)");
        // send_message(stream, "FILE_REQUEST:hiroshi.png:::END_OF_HEADER");
        // send_message(stream, "FILE_REQUEST:hiroshi.png:7679671:END_OF_HEADER");
        send_message(stream, &message);
        return Ok(());
    }
}
pub fn process_file_request_response(
    stream: &mut TcpStream,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) -> io::Result<()> {
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

    let mut file = File::create(&file_path)?;
    let mut buffer = vec![0; 4096];
    let mut total_bytes_read = 0;
    // convert file size to usize
    let _file_size = _file_size.parse::<usize>().unwrap();

    while total_bytes_read < _file_size {
        let bytes_read = stream.read(&mut buffer)?;
        if bytes_read == 0 {
            break; // Connection closed
        }
        total_bytes_read += bytes_read;
        file.write_all(&buffer[..bytes_read])?;
    }
    // Ensure all data is written to the file
    file.flush()?;

    println!("File received and saved to {:?}", file_path);
    Ok(())
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
