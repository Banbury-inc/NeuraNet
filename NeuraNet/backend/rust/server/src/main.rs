extern crate tokio;
extern crate tungstenite;
extern crate url;
use handlers::database_handler;
use handlers::login_handler;
use std::collections::HashMap;

use std::sync::Arc;
use std::thread;
use tokio::net::TcpListener;
use tokio::net::TcpStream;
use tokio::sync::Mutex;
use tokio::task;
use tungstenite::accept_hdr;
use tungstenite::handshake::server::{Request, Response};
mod handlers;
use handlers::client_handler::handle_connection;
use handlers::file_handler;

pub type ClientsList = Arc<Mutex<HashMap<String, Vec<Arc<Mutex<TcpStream>>>>>>;

#[tokio::main]
async fn main() {
    if let Err(e) = initialize_database().await {
        println!("Error initializing database: {}", e);
        return;
    }

    println!("Welcome to the Banbury NeuraNet");
    // Start the async server
    let listener = TcpListener::bind("127.0.0.1:443").await.unwrap();
    // let clients = Arc::new(Mutex::new(Vec::new()));
    let clients = Arc::new(Mutex::new(HashMap::new()));
    loop {
        let (stream, address) = listener.accept().await.unwrap();
        
        println!("Connection established");
        let clients = Arc::clone(&clients);
        println!("Client count: {}", clients.lock().await.len());
        println!("Client address: {}", address);
        tokio::spawn(async move {
            handle_connection(stream, clients).await;
        });
    }
}

async fn initialize_database() -> mongodb::error::Result<()> {
    database_handler::get_total_data_processed().await?;
    database_handler::get_total_requests_processed().await?;
    println!("Initializing Database...");
    database_handler::initialize().await?;
    println!("Database Initialized");
    Ok(())
}
