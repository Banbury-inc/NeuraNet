use std::net::TcpListener;
use std::{fs, thread, time::Duration};
use tungstenite::accept;
extern crate tungstenite;

fn handle_connection(mut websocket: tungstenite::protocol::WebSocket<std::net::TcpStream>) {
    let msg = websocket.read_message().expect("Error reading message");
    let request_line = msg.to_text().unwrap();

    let (status_line, filename) = match request_line {
        "GET /" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );

    websocket
        .write_message(tungstenite::Message::Text(response))
        .unwrap();
}

fn main() {
    println!("Welcome to the Banbury NeuraNet");
    let listener = TcpListener::bind("127.0.0.1:443").unwrap();

    for stream in listener.incoming() {
        println!("Connection established");
        let stream = stream.unwrap();

        thread::spawn(|| {
            let websocket = accept(stream).expect("Failed to accept connection");
            handle_connection(websocket);
        });
    }
}
