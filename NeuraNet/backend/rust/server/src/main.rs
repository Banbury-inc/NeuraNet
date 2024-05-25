extern crate tungstenite;
extern crate url;
use handlers::database_handler;
use std::net::TcpListener;
use std::sync::{Arc, Mutex};
use std::thread;
use tungstenite::accept_hdr;
use tungstenite::handshake::server::{Request, Response};
// test
mod handlers;
use handlers::client_handler::handle_connection;

fn main() {
    println!("Welcome to the Banbury NeuraNet");
    let listener = TcpListener::bind("127.0.0.1:443").unwrap();
    let clients = Arc::new(Mutex::new(Vec::new()));
    println!("Initializing Database...");
    database_handler::initialize();
    println!("Database Initialized");
    database_handler::get_total_data_processed().unwrap();
    for stream in listener.incoming() {
        println!("Connection established");
        let stream = stream.unwrap();
        let clients = Arc::clone(&clients);

        thread::spawn(move || {
            handle_connection(stream, clients);
        });
    }
}
