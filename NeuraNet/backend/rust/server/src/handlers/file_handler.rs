use super::database_handler::{self, Users};
use super::ping_handler::send_message;
use mongodb::{bson::doc, options::ClientOptions, Client, Collection};
use std::path::Path;
use std::sync::Arc;
use tokio::fs::{self, File};
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::sync::Mutex;

async fn get_client() -> mongodb::error::Result<Client> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client_options = ClientOptions::parse(uri).await?;
    let client = Client::with_options(client_options)?;
    Ok(client)
}

pub async fn process_file(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    let directory_name = "NeuraNet_File_Directory";
    let directory_path = format!(
        "{}/{}",
        std::env::current_dir().unwrap().to_str().unwrap(),
        directory_name
    );
    let file_path = format!("{}/{}", directory_name, file_name);

    if !Path::new(&directory_path).exists() {
        println!("Directory does not exist, creating directory");
        fs::create_dir(&directory_path).await.unwrap();
    }

    println!("Receiving file...");

    let mut file = File::create(&file_path).await.unwrap();
    file.write_all(buffer.as_bytes()).await.unwrap();

    println!("File received and saved to {:?}", file_path);
}

pub async fn process_file_request(
    buffer: &str,
    stream: Arc<Mutex<TcpStream>>,
    file_name: &str,
    file_size: &str,
    username: &str,
) -> mongodb::error::Result<()> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");
    println!("Received file request");

    let user = database_handler::get_user(username).await.unwrap();

    let message = format!("FILE_REQUEST:{}:{}:END_OF_HEADER", file_name, file_size);

    if user.is_none() {
        println!("User does not exist");
        return Ok(());
    } else {
        println!("sending file request :)");
        let mut stream_guard = stream.lock().await;
        send_message(&mut *stream_guard, &message).await;
        return Ok(());
    }
}

pub async fn process_file_request_response(
    stream: &mut TcpStream,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) -> io::Result<()> {
    println!("Received file request response");
    let directory_name = "NeuraNet_File_Directory";
    let directory_path = format!(
        "{}/{}",
        std::env::current_dir().unwrap().to_str().unwrap(),
        directory_name
    );
    let file_path = format!("{}/{}", directory_name, file_name);

    if !Path::new(&directory_path).exists() {
        println!("Directory does not exist, creating directory");
        fs::create_dir(&directory_path).await.unwrap();
    }
    println!("Receiving file...");

    let mut file = File::create(&file_path).await?;
    let mut buffer = vec![0; 4096];
    let mut total_bytes_read = 0;
    let file_size = file_size.parse::<usize>().unwrap();

    while total_bytes_read < file_size {
        let bytes_read = stream.read(&mut buffer).await?;
        if bytes_read == 0 {
            break; // Connection closed
        }
        total_bytes_read += bytes_read;
        file.write_all(&buffer[..bytes_read]).await?;
    }
    file.flush().await?;

    println!("File received and saved to {:?}", file_path);

    println!("Broadcasting to other devices");

    Ok(())
}

pub async fn process_file_delete_request(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received file delete request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}

pub async fn process_file_delete_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    file_name: &str,
    device_name: &str,
    file_size: &str,
) {
    println!("Received file delete request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}

