use super::database_handler::{self, Users};
use super::ping_handler::send_message;
use mongodb::options::ClientOptions;
use mongodb::{bson::doc, Client, Collection};
use tokio::io::AsyncWriteExt;
use tokio::net::TcpStream;

async fn get_client() -> mongodb::error::Result<Client> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client_options = ClientOptions::parse(uri).await?;
    let client = Client::with_options(client_options)?;
    Ok(client)
}

pub async fn process_login_request(
    _buffer: &str,
    stream: &mut TcpStream,
    username: &str,
    password: &str,
) -> mongodb::error::Result<()> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");
    println!("Received login request");

    let user = database_handler::get_user(username).await.unwrap();

    // check if the user exists
    if user.is_none() {
        println!("User does not exist");
        send_message(stream, "LOGIN_FAIL:").await?;
    } else {
        println!("User exists");
        send_message(stream, "LOGIN_SUCCESS:").await?;
    }
    Ok(())
}
