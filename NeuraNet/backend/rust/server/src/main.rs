extern crate tokio;
extern crate tungstenite;
extern crate url;
use handlers::database_handler;
use handlers::login_handler;
use std::sync::Arc;
use std::thread;
use tokio::net::TcpListener;
use tokio::sync::Mutex;
use tokio::task;
use tungstenite::accept_hdr;
use tungstenite::handshake::server::{Request, Response};
mod handlers;
use handlers::client_handler::handle_connection;

#[tokio::main]
async fn main() {
    println!("Welcome to the Banbury NeuraNet");

    // Initialize the database
    if let Err(e) = initialize_database().await {
        println!("Error initializing database: {}", e);
        return;
    }

    // Start the async server
    let listener = TcpListener::bind("127.0.0.1:443").await.unwrap();
    let clients = Arc::new(Mutex::new(Vec::new()));
    loop {
        let (stream, _) = listener.accept().await.unwrap();
        println!("Connection established");
        let clients = Arc::clone(&clients);
        println!("Stream: {:?}", stream);

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
