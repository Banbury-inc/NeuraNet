use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;
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
