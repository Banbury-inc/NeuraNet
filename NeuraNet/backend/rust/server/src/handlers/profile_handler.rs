use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_change_profile_request(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received change_profile_request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
