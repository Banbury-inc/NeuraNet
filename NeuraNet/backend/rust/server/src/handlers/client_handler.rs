extern crate tungstenite;
extern crate url;
use super::ping_handler::send_ping;
use std::sync::{Arc, Mutex};
use tungstenite::protocol::WebSocket;

pub fn handle_connection(
    websocket: WebSocket<std::net::TcpStream>,
    clients: Arc<Mutex<Vec<WebSocket<std::net::TcpStream>>>>,
) {
    let peer_addr = websocket.get_ref().peer_addr().unwrap();

    {
        let mut clients_guard = clients.lock().unwrap();
        clients_guard.push(websocket);
    }

    loop {
        let mut clients_guard = clients.lock().unwrap();
        let websocket_option = clients_guard
            .iter_mut()
            .find(|ws| ws.get_ref().peer_addr().unwrap() == peer_addr);

        if let Some(websocket) = websocket_option {
            match websocket.read_message() {
                Ok(_msg) => {
                    send_ping(websocket);
                }
                Err(e) => {
                    println!("Error reading message: {:?}", e);
                    break;
                }
            }
        } else {
            break;
        }
    }

    {
        let mut clients_guard = clients.lock().unwrap();
        clients_guard.retain(|ws| ws.get_ref().peer_addr().unwrap() != peer_addr);
    }
}
