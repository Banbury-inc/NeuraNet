extern crate tungstenite;
extern crate url;
use super::database_handler;
use super::device_handler;
use super::device_handler::ClientList;
use super::file_handler;
use super::login_handler;
use super::message_handler;
use super::ping_handler;
use super::profile_handler;
use super::registration_handler;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{self, split, AsyncReadExt, AsyncWriteExt, Error, WriteHalf};

use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio::sync::MutexGuard;
use tokio::task;
use tokio::time::timeout;
use tokio::time::{sleep, Duration};

// pub type ClientList = Arc<Mutex<HashMap<String, Vec<Arc<Mutex<TcpStream>>>>>>;

// Define the function to be async and to return a Result
// Function to read all bytes from the stream
// Function to read all bytes from the stream and return them as a Vec<u8>
async fn read_all_bytes(mut stream: MutexGuard<'_, TcpStream>) -> Result<Vec<u8>, Error> {
    let mut buffer = vec![0; 4096];
    let mut data = Vec::new();
    while let Some(bytes_read) = stream.read(&mut buffer).await.ok() {
        if bytes_read == 0 {
            break;
        }
        data.extend_from_slice(&buffer[..bytes_read]);
    }
    Ok(data)
}

// Function to read and parse a message from a TcpStream
async fn read_message(stream: Arc<Mutex<TcpStream>>) -> Result<String, Error> {
    let mut stream_lock = stream.lock().await;
    let data = read_all_bytes(stream_lock).await?;
    String::from_utf8(data).map_err(|e| Error::new(tokio::io::ErrorKind::InvalidData, e))
}
pub async fn read_bytes(
    reader: &mut (impl AsyncReadExt + Unpin),
    buffer: &mut [u8],
) -> Result<usize, Error> {
    reader.read(buffer).await
}

pub async fn handle_connection(stream: TcpStream, clients: ClientList) -> io::Result<()> {
    let (mut reader, writer) = split(stream);
    let writer = Arc::new(Mutex::new(writer));
    let mut buffer = [0; 4096];
    loop {
        let bytes_read;
        {
            // bytes_read = reader.read(&mut buffer).await?;
            bytes_read = read_bytes(&mut reader, &mut buffer).await?;
        }
        if bytes_read == 0 {
            return Ok(());
        }
        // Convert the message to a String
        let message: String = String::from_utf8_lossy(&buffer[..bytes_read]).to_string();
        println!("Received message: {}", message);

        // Process the message
        process_message(
            message,
            &mut buffer,
            &mut reader,
            Arc::clone(&writer),
            Arc::clone(&clients),
        )
        .await;
    }
}

// Example function to process a message
pub async fn process_message(
    message: String,
    buffer: &mut [u8],
    reader: &mut (impl AsyncReadExt + Unpin),
    stream: Arc<Mutex<WriteHalf<TcpStream>>>,
    clients: ClientList,
) {
    // Placeholder for further processing, for example:
    // Detect message type, handle accordingly.
    let end_of_header = "END_OF_HEADER";

    if message.contains(end_of_header) {
        let parts: Vec<&str> = message.split(end_of_header).collect();
        let header = parts[0];
        let buffer_str = parts[1];
        println!("Header: {}", header);

        let header_parts: Vec<&str> = header.split(':').collect();
        if header_parts.len() < 4 {
            println!("Malformed header: {}", header);
        }
        let file_type = header_parts[0];
        let file_name = header_parts[1];
        let device_name = header_parts[1];
        let file_size = header_parts[2];
        let username = header_parts[3];
        let password = header_parts[3];

        match file_type {
            "GREETINGS" => {
                // println!("Received greetings from {}", client_id);
                println!("1");
                let stream_clone = Arc::clone(&stream);
                tokio::spawn(async move {
                    ping_handler::begin_single_small_ping_loop(stream_clone);
                });
                let stream_clone2 = Arc::clone(&stream);
                tokio::spawn(async move {
                    ping_handler::begin_single_ping_loop(stream_clone2);
                });
            }

            "MSG" => message_handler::process_message_request(buffer_str, username, password).await,

            "REGISTRATION_REQUEST" => {
                registration_handler::process_registration_request(buffer_str, username, password)
                    .await
            }
            "FILE" => {
                file_handler::process_file(
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            "FILE_REQUEST" => {
                if let Err(e) = file_handler::process_file_request(
                    buffer_str, stream, file_name, file_size, username,
                )
                .await
                {
                    println!("Error processing file request: {:?}", e);
                }
            }

            "FILE_REQUEST_RESPONSE" => {
                if let Err(e) = file_handler::process_file_request_response(
                    stream,
                    reader,
                    buffer,
                    file_name,
                    device_name,
                    file_size,
                    Arc::clone(&clients),
                )
                .await
                {
                    println!("File request failed: {}", e);
                }
            }
            "DEVICE_DELETE_REQUEST" => {
                device_handler::process_device_delete_request(
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            "FILE_DELETE_REQUEST" => {
                file_handler::process_file_delete_request(
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            "FILE_DELETE_REQUEST_RESPONSE" => {
                file_handler::process_file_delete_request_response(
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            "CHANGE_PROFILE_REQUEST" => {
                profile_handler::process_change_profile_request(
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            "SMALL_PING_REQUEST_RESPONSE" => {
                ping_handler::process_small_ping_request_response(stream, buffer_str).await
            }
            "PING_REQUEST_RESPONSE" => {
                ping_handler::process_ping_request_response(
                    stream,
                    buffer_str,
                    username,
                    password,
                    file_name,
                    device_name,
                    file_size,
                )
                .await
            }
            _ => println!("Unknown file type: {}", file_type),
        }
    } else {
        println!("Received unknown file type");
    }
}

async fn remove_client_from_list(
    client_id: String,
    clients: ClientList,
    client: Arc<Mutex<TcpStream>>,
) {
    let mut clients_guard = clients.lock().await;
    if let Some(client_list) = clients_guard.get_mut(&client_id) {
        if let Some(pos) = client_list.iter().position(|x| Arc::ptr_eq(x, &client)) {
            client_list.remove(pos);
            if client_list.is_empty() {
                // Drop the mutable borrow before removing the entry
                drop(client_list);
                clients_guard.remove(&client_id);
            } else {
                println!(
                    "Connection removed. Total connections for {}: {}",
                    client_id,
                    client_list.len()
                );
            }
        }
    }
}

fn get_client_id(stream: &TcpStream) -> String {
    // Implement your logic to determine the client ID
    // For example, use the peer address or a unique identifier sent by the client
    stream.peer_addr().unwrap().to_string()
}
