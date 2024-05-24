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
use std::sync::{Arc, Mutex};
use tungstenite::protocol::WebSocket;
use tungstenite::Message;
pub fn handle_connection(
    websocket: WebSocket<std::net::TcpStream>,
    clients: Arc<Mutex<Vec<WebSocket<std::net::TcpStream>>>>,
) {
    let peer_addr = websocket.get_ref().peer_addr().unwrap();

    {
        let mut clients_guard = clients.lock().unwrap();
        clients_guard.push(websocket);
    }

    loop {
        let mut clients_guard = clients.lock().unwrap();
        let websocket_option = clients_guard
            .iter_mut()
            .find(|ws| ws.get_ref().peer_addr().unwrap() == peer_addr);

        if let Some(websocket) = websocket_option {
            match websocket.read_message() {
                Ok(_msg) => {
                    match _msg {
                        Message::Binary(_bin) => {
                            println!("Received binary message");
                        }
                        Message::Ping(_ping) => {
                            println!("Received ping");
                        }
                        Message::Pong(_pong) => {
                            println!("Received pong");
                        }
                        Message::Close(_close) => {
                            println!("Received close");
                            break;
                        }
                        Message::Text(_msg) => {
                            println!("Received: {}", _msg);
                            // Parse the message
                            let end_of_header = "END_OF_HEADER:";
                            let buffer = _msg;
                            if buffer.contains(end_of_header) {
                                let parts: Vec<&str> = buffer.split(end_of_header).collect();
                                let header = parts[0];
                                let buffer = parts[1];
                                println!("Header: {}", header);
                                println!("Buffer: {}", buffer);

                                let parts: Vec<&str> = header.split(':').collect();
                                let file_type = parts[0];
                                let file_name = parts[1];
                                let device_name = parts[1];
                                let file_size = parts[2];
                                let password = parts[2];
                                let username = parts[3];
                                println!("File type: {}", file_type);
                                println!("File name: {}", file_name);
                                println!("File size: {}", file_size);
                                println!("Username: {}", username);
                                println!("Password: {}", password);
                                if file_type == "MSG" {
                                    message_handler::process_message_request(
                                        buffer, username, password,
                                    );
                                }
                                if file_type == "LOGIN_REQUEST" {
                                    login_handler::process_login_request(
                                        buffer, username, password,
                                    );
                                }
                                if file_type == "REGISTRATION_REQUEST" {
                                    registration_handler::process_registration_request(
                                        buffer, username, password,
                                    );
                                }
                                if file_type == "FILE" {
                                    file_handler::process_file(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "FILE_REQUEST" {
                                    file_handler::process_file_request(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "FILE_REQUEST_RESPONSE" {
                                    file_handler::process_file_request_response(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "DEVICE_DELETE_REQUEST" {
                                    device_handler::process_device_delete_request(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "FILE_DELETE_REQUEST" {
                                    file_handler::process_file_delete_request(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "FILE_DELETE_REQUEST_RESPONSE" {
                                    file_handler::process_file_delete_request_response(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "CHANGE_PROFILE_REQUEST" {
                                    profile_handler::process_change_profile_request(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "SMALL_PING_REQUEST_RESPONSE" {
                                    ping_handler::process_small_ping_request_response(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                                if file_type == "PING_REQUEST_RESPONSE" {
                                    ping_handler::process_ping_request_response(
                                        buffer,
                                        username,
                                        password,
                                        file_name,
                                        device_name,
                                        file_size,
                                    );
                                }
                            }
                        }

                        Message::Frame(_bin) => {
                            println!("Received binary message");
                        }
                    }
                }
                Err(e) => {
                    println!("Error reading message: {:?}", e);
                    break;
                }
            }
        } else {
            break;
        }
    }

    {
        let mut clients_guard = clients.lock().unwrap();
        clients_guard.retain(|ws| ws.get_ref().peer_addr().unwrap() != peer_addr);
    }
}
