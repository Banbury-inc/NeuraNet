use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn send_ping(websocket: &mut WebSocket<std::net::TcpStream>) {
    loop {
        // set a timer for 5 seconds
        thread::sleep(std::time::Duration::from_secs(5));
        send_message(websocket, "Hello, receiver!");
    }
    // if _msg.is_close() {
    // break;
    // }
}

pub fn send_message(websocket: &mut WebSocket<std::net::TcpStream>, message: &str) {
    let message = Message::Text(message.to_string());
    if let Err(e) = websocket.write_message(message) {
        println!("Error sending message: {:?}", e);
    }
}

pub fn process_small_ping_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received small ping request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
pub fn process_ping_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received ping request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
