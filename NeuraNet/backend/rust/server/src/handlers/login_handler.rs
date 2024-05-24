use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn process_login_request(buffer: &str, username: &str, password: &str) {
    println!("Received login request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
