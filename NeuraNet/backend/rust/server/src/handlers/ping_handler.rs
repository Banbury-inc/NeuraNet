use serde_json::Value;
use std::io::{Result, Write};
use std::net::TcpStream;
use std::thread;
use tungstenite::protocol::WebSocket;
use tungstenite::Message;

pub fn begin_small_ping_loop(stream: &mut TcpStream) {
    loop {
        // set a timer for 5 seconds
        thread::sleep(std::time::Duration::from_secs(5));
        println!("Sending small ping request");
        send_message(stream, "SMALL_PING_REQUEST:::END_OF_HEADER");
    }
}
pub fn begin_ping_loop(stream: &mut TcpStream) {
    loop {
        // set a timer for 5 seconds
        thread::sleep(std::time::Duration::from_secs(600));
        send_message(stream, "PING_REQUEST:::END_OF_HEADER");
    }
}

pub fn send_message(stream: &mut TcpStream, message: &str) -> Result<()> {
    stream.write_all(message.as_bytes())
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
    let end_of_json = "END_OF_JSON";

    if buffer.contains(end_of_json) {
        let parts: Vec<&str> = buffer.split(end_of_json).collect();
        let json_content = parts[0];
        let json_trash = parts[1];

        // Parse the JSON buffer
        let json_value: Value = serde_json::from_str(json_content).expect("Invalid JSON");

        // Extract specific values from the JSON
        let username = json_value
            .get("user")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let device_name = json_value
            .get("device_name")
            .and_then(Value::as_i64)
            .unwrap_or_default();
        let files = json_value
            .get("files")
            .and_then(Value::as_str)
            .unwrap_or_default();

        // Print extracted values
        println!("User: {}", username);
        println!("Device Number: {}", device_name);
        println!("File Path: {}", files);
    }
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
