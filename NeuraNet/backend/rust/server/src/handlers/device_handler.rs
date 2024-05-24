use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_device_delete_request(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received file request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
