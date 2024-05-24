use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_change_profile_request(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received change_profile_request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
