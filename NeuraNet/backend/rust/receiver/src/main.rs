extern crate tungstenite;
extern crate url;

use tungstenite::{connect, Message};
use url::Url;

fn main() {
    // Connect to the WebSocket server
    let (mut socket, response) =
        connect(Url::parse("ws://127.0.0.1:443").unwrap()).expect("Can't connect");

    println!("Connected to the server");
    println!("Response HTTP code: {}", response.status());
    println!("Response contains the following headers:");
    for (ref header, ref header_value) in response.headers() {
        println!("* {}: {:?}", header, header_value);
    }

    let file_name = "test.txt";
    let file_size = "1000";
    let password = "password";
    let username = "user_name";
    let end_of_header = "END_OF_HEADER";
    let content = "Hello, relay server!";
    let message = format!(
        "MSG:{}:{}:{}:{}:{}:{}",
        file_name, file_size, password, username, end_of_header, content
    );
    // Send a message to the server
    socket.write_message(Message::Text(message)).unwrap();

    // Loop to keep the connection open and continuously read messages
    loop {
        match socket.read_message() {
            Ok(msg) => {
                println!("Received: {}", msg);
                // Optionally, respond to the server or handle the message
            }
            Err(e) => {
                println!("Error reading message: {:?}", e);
                break;
            }
        }
    }

    println!("Connection closed.");
}
