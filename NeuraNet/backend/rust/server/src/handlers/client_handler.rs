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
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio::task;

pub async fn handle_connection(stream: TcpStream, clients: Arc<Mutex<Vec<Arc<Mutex<TcpStream>>>>>) {
    let stream = Arc::new(Mutex::new(stream));
    // let client = Arc::new(Mutex::new(stream));
    let client = Arc::clone(&stream);
    {
        let mut clients_guard = clients.lock().await;
        clients_guard.push(client.clone());
        println!("New client added. Total clients: {}", clients_guard.len());
    }
    let mut buffer_size = vec![0; 4096];

    // Spawn new async tasks for the ping handler
    let small_ping_stream = Arc::clone(&stream);
    let ping_stream = Arc::clone(&stream);
    let broadcast_clients = Arc::clone(&clients);
    task::spawn(async move {
        ping_handler::begin_small_ping_loop(small_ping_stream).await;
    });
    task::spawn(async move {
        ping_handler::begin_ping_loop(ping_stream).await;
    });

    loop {
        let mut stream_guard = stream.lock().await;
        match stream_guard.read(&mut buffer_size).await {
            Ok(bytes_read) => {
                database_handler::update_total_data_processed(bytes_read).await;
                database_handler::update_number_of_requests_processed().await;
                if bytes_read == 0 {
                    // connection closed by client
                    println!("Connection closed by client");
                    break;
                }
                // println!("Received: {} bytes", bytes_read);
                let buffer = String::from_utf8_lossy(&buffer_size[..bytes_read]);
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
                                stream.clone(),
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

    // Remove client from the list
    let mut clients_guard = clients.lock().await;
    if let Some(pos) = clients_guard.iter().position(|x| Arc::ptr_eq(x, &stream)) {
        clients_guard.remove(pos);
    }
    println!("Client disconnected");
}
