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

    // Send a message to the server
    socket.write_message(Message::Text("GET /".into())).unwrap();
    println!("Sent message to the server");

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
