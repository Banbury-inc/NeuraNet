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
use calldb::call_get_some_data;
use handlers::client_handler::handle_connection;
use handlers::database_handler::{connect_to_mongodb, get_some_data};

use crate::calldb::call_get_devices;
use crate::calldb::call_get_user;
use crate::calldb::call_initialize;

fn main() {
    println!("Welcome to the Banbury NeuraNet");
    let listener = TcpListener::bind("127.0.0.1:443").unwrap();
    let clients = Arc::new(Mutex::new(Vec::new()));
    println!("Initializing Database...");
    call_initialize().unwrap();

    // test functions
    // call_get_devices().unwrap();
    // call_get_user().unwrap();
    for stream in listener.incoming() {
        println!("Connection established");
        let stream = stream.unwrap();
        let clients = Arc::clone(&clients);

        thread::spawn(move || {
            handle_connection(stream, clients);
        });
    }
}
