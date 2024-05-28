use super::database_handler::Users;
use super::ping_handler::send_message;
use crate::handlers::database_handler;

use mongodb::{
    bson::doc,
    sync::{Client, Collection},
};
use std::net::TcpStream;

pub fn process_login_request(
    _buffer: &str,
    stream: &mut TcpStream,
    username: &str,
    password: &str,
) -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");
    println!("Received login request");

    let user = database_handler::get_user(username).unwrap();
    // println!("User: {:?}", user);

    // check if the user exists
    if user.is_none() {
        println!("User does not exist");
        send_message(stream, "LOGIN_FAIL:");
        return Ok(());
    } else {
        println!("User exists");
        send_message(stream, "LOGIN_SUCCESS:");
        return Ok(());
    }
}
