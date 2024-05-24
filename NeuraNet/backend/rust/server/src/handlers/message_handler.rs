use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_message_request(buffer: &str, username: &str, password: &str) {
    println!("Received message request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
