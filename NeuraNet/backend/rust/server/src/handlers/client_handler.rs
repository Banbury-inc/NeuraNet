extern crate tungstenite;
extern crate url;
use super::client_handler;
use super::database_handler;
use super::device_handler;
use super::file_handler;
use super::login_handler;
use super::message_handler;
use super::ping_handler;
use super::profile_handler;
use super::registration_handler;
use std::io::{Read, Write};
use std::net::TcpStream;
use std::sync::{Arc, Mutex};
use std::thread;

pub fn handle_connection(mut stream: TcpStream, clients: Arc<Mutex<Vec<std::net::TcpStream>>>) {
    let mut buffer_size = vec![0; 4096];
    // Spawn a new thread for the ping handler
    let mut ping_stream = stream.try_clone().expect("Failed to clone TcpStream");
    thread::spawn(move || {
        ping_handler::begin_small_ping_loop(&mut ping_stream);
    });
    loop {
        match stream.read(&mut buffer_size) {
            Ok(bytes_read) => {
                database_handler::update_total_data_processed(bytes_read).unwrap();
                if bytes_read == 0 {
                    // connection closed by client
                    println!("Connection closed by client");
                    break;
                }
                // println!("Received: {} bytes", bytes_read);
                let buffer = String::from_utf8_lossy(&buffer_size[..bytes_read]);
                println!("Received: {}", buffer);
                let end_of_header = "END_OF_HEADER";

                if buffer.contains(end_of_header) {
                    let parts: Vec<&str> = buffer.split(end_of_header).collect();
                    let header = parts[0];
                    let buffer = parts[1];
                    println!("Header: {}", header);
                    println!("Buffer: {}", buffer);

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
                        }
                        "LOGIN_REQUEST" => {
                            login_handler::process_login_request(buffer, username, password)
                        }
                        "REGISTRATION_REQUEST" => {
                            registration_handler::process_registration_request(
                                buffer, username, password,
                            )
                        }
                        "FILE" => file_handler::process_file(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
                        "FILE_REQUEST" => file_handler::process_file_request(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
                        "FILE_REQUEST_RESPONSE" => file_handler::process_file_request_response(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
                        "DEVICE_DELETE_REQUEST" => device_handler::process_device_delete_request(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
                        "FILE_DELETE_REQUEST" => file_handler::process_file_delete_request(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
                        "FILE_DELETE_REQUEST_RESPONSE" => {
                            file_handler::process_file_delete_request_response(
                                buffer,
                                username,
                                password,
                                file_name,
                                device_name,
                                file_size,
                            )
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
                        }
                        "SMALL_PING_REQUEST_RESPONSE" => {
                            ping_handler::process_small_ping_request_response(
                                buffer,
                                username,
                                password,
                                file_name,
                                device_name,
                                file_size,
                            )
                        }
                        "PING_REQUEST_RESPONSE" => ping_handler::process_ping_request_response(
                            buffer,
                            username,
                            password,
                            file_name,
                            device_name,
                            file_size,
                        ),
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

    let mut clients_lock = clients.lock().unwrap();
    clients_lock.retain(|client| client.peer_addr().ok() != stream.peer_addr().ok());
}
