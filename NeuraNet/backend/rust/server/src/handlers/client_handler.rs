extern crate tungstenite;
extern crate url;
use super::database_handler;
use super::device_handler;
use super::file_handler;
use super::login_handler;
use super::message_handler;
use super::ping_handler;
use super::profile_handler;
use super::registration_handler;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio::task;
use tokio::time::{sleep, Duration};

pub type ClientList = Arc<Mutex<HashMap<String, Vec<Arc<Mutex<TcpStream>>>>>>;

pub async fn handle_connection(stream: TcpStream, clients: ClientList) {
    let client_id = get_client_id(&stream); // Function to determine client ID
    let client = Arc::new(Mutex::new(stream));
    let client_clone = Arc::clone(&client);
    // Add the client to the client's connection list
    {
        let mut clients_guard = clients.lock().await;
        let entry = clients_guard
            .entry(client_id.clone())
            .or_insert_with(Vec::new);
        entry.push(client.clone());
        println!(
            "New connection added. Total connections for {}: {}",
            client_id,
            entry.len()
        );
    }

    let mut buffer_size = vec![0; 4096];
    // Spawn new async tasks for the ping handler
    // Spawn new async tasks for the ping handler
    loop {
        let mut stream_guard = client.lock().await;
        match stream_guard.read(&mut buffer_size).await {
            Ok(bytes_read) => {
                database_handler::update_total_data_processed(bytes_read).await;
                database_handler::update_number_of_requests_processed().await;
                if bytes_read == 0 {
                    // connection closed by client
                    println!("connection closed by client");
                    // continue;
                    break;
                }
                println!("Received: {} bytes", bytes_read);
                let buffer = String::from_utf8_lossy(&buffer_size[..bytes_read]);
                println!("Buffer: {}", buffer);
                let end_of_header = "END_OF_HEADER";

                if buffer.contains(end_of_header) {
                    let parts: Vec<&str> = buffer.split(end_of_header).collect();
                    let header = parts[0];
                    let buffer = parts[1];
                    println!("Header: {}", header);
                    // println!("Buffer: {}", buffer);

                    let header_parts: Vec<&str> = header.split(':').collect();
                    if header_parts.len() < 4 {
                        println!("Malformed header: {}", header);
                        continue;
                    }

                    let file_type = header_parts[0];
                    let file_name = header_parts[1];
                    let device_name = header_parts[1];
                    let file_size = header_parts[2];
                    let username = header_parts[3];
                    let password = header_parts[3];
                    match file_type {
                        "GREETINGS" => {
                            let client_clone = Arc::clone(&client);
                            tokio::spawn(async move {
                                loop {
                                    println!("1");
                                    {
                                        let mut stream_guard = client_clone.lock().await;
                                        println!("2");
                                        let message = "SMALL_PING_REQUEST:::END_OF_HEADER";
                                        println!("3");
                                        if let Err(e) =
                                            stream_guard.write_all(message.as_bytes()).await
                                        {
                                            println!("Failed to send message: {:?}", e);
                                            break;
                                        }
                                    }
                                    println!("4");
                                    sleep(Duration::from_secs(5)).await;
                                    println!("Sent small ping request");
                                }
                            });
                            let client_clone_2 = Arc::clone(&client);
                            tokio::spawn(async move {
                                loop {
                                    println!("1");
                                    {
                                        let mut stream_guard = client_clone_2.lock().await;
                                        println!("2");
                                        let message = "PING_REQUEST:::END_OF_HEADER";
                                        println!("3");
                                        if let Err(e) =
                                            stream_guard.write_all(message.as_bytes()).await
                                        {
                                            println!("Failed to send message: {:?}", e);
                                            break;
                                        }
                                    }
                                    println!("4");
                                    sleep(Duration::from_secs(10)).await;
                                    println!("Sent ping request");
                                }
                            });
                        }

                        "MSG" => {
                            message_handler::process_message_request(buffer, username, password)
                                .await
                        }

                        "LOGIN_REQUEST" => {
                            if let Err(e) = login_handler::process_login_request(
                                buffer,
                                &mut *stream_guard,
                                username,
                                password,
                            )
                            .await
                            {
                                println!("Error processing login request: {:?}", e);
                            }
                        }
                        "REGISTRATION_REQUEST" => {
                            registration_handler::process_registration_request(
                                buffer, username, password,
                            )
                            .await
                        }
                        "FILE" => {
                            file_handler::process_file(
                                buffer,
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
                                buffer,
                                &mut *stream_guard,
                                file_name,
                                file_size,
                                username,
                            )
                            .await
                            {
                                println!("Error processing file request: {:?}", e);
                            }
                        }

                        "FILE_REQUEST_RESPONSE" => {
                            if let Err(e) = file_handler::process_file_request_response(
                                // Arc::clone(&stream),
                                &mut *stream_guard,
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
                                buffer,
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
                                buffer,
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
                                buffer,
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
                                buffer,
                                username,
                                password,
                                file_name,
                                device_name,
                                file_size,
                            )
                            .await
                        }
                        "SMALL_PING_REQUEST_RESPONSE" => {
                            ping_handler::process_small_ping_request_response(
                                Arc::clone(&client),
                                buffer,
                            )
                            .await
                        }
                        "PING_REQUEST_RESPONSE" => {
                            println!("Received ping request response");
                            ping_handler::process_ping_request_response(
                                buffer,
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
            Err(e) => {
                println!("Error reading message: {:?}", e);
                break;
            }
        }
    }

    // Remove the client from the list
    remove_client_from_list(client_id, clients, client).await;
    println!("Client disconnected");
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
