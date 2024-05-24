use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_registration_request(buffer: &str, username: &str, password: &str) {
    println!("Received registration request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
