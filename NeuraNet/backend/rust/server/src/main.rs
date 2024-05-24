extern crate tungstenite;
extern crate url;

use std::net::TcpListener;
use std::sync::{Arc, Mutex};
use std::thread;
use tungstenite::accept_hdr;
use tungstenite::handshake::server::{Request, Response};
// test
mod calldb;
mod handlers;
use calldb::calldb;
use handlers::client_handler::handle_connection;
use handlers::database_handler::{connect_to_mongodb, get_some_data};

fn main() {
    println!("Welcome to the Banbury NeuraNet WebSocket server");
    let listener = TcpListener::bind("127.0.0.1:443").unwrap();
    let clients = Arc::new(Mutex::new(Vec::new()));
    let database_info = calldb().unwrap();
    for stream in listener.incoming() {
        println!("Connection established");
        let stream = stream.unwrap();
        let clients = Arc::clone(&clients);

        thread::spawn(move || {
            let callback = |req: &Request, mut response: Response| {
                println!("Received request: {:?}", req); // Use {:?} to print debug info
                                                         // Add an additional header to the response
                response
                    .headers_mut()
                    .append("X-Custom-Header", "BanburyNeuraNet".parse().unwrap());
                Ok(response)
            };
            let websocket = accept_hdr(stream, callback).expect("Failed to accept connection");

            handle_connection(websocket, clients);
        });
    }
}
