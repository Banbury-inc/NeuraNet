extern crate tungstenite;
extern crate url;
use handlers::database_handler;
use handlers::login_handler;
use std::net::TcpListener;
use std::sync::{Arc, Mutex};
use std::thread;
use tungstenite::accept_hdr;
use tungstenite::handshake::server::{Request, Response};
// test
mod handlers;
use handlers::client_handler::handle_connection;
use handlers::file_handler::process_file;

use crate::handlers::file_handler;

fn main() {
    println!("Welcome to the Banbury NeuraNet");
    let listener = TcpListener::bind("127.0.0.1:443").unwrap();
    let clients = Arc::new(Mutex::new(Vec::new()));
    database_handler::get_total_data_processed().unwrap();
    println!("Initializing Database...");
    database_handler::initialize();
    println!("Database Initialized");
    for stream in listener.incoming() {
        println!("Connection established");
        let stream = stream.unwrap();
        let clients = Arc::clone(&clients);

        thread::spawn(move || {
            handle_connection(stream, clients);
        });
    }
}
