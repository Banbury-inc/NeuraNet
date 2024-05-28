use super::database_handler;
use super::database_handler::Files;
use serde_json::from_value;
use serde_json::Value;
use std::io::{Result, Write};
use std::net::TcpStream;
use std::thread;

pub fn begin_small_ping_loop(stream: &mut TcpStream) {
    loop {
        // set a timer for 5 seconds
        // println!("Sending small ping request");
        send_message(stream, "SMALL_PING_REQUEST:::END_OF_HEADER");
        thread::sleep(std::time::Duration::from_secs(30));
    }
}
pub fn begin_ping_loop(stream: &mut TcpStream) {
    loop {
        // set a timer for 5 seconds
        send_message(stream, "PING_REQUEST:::END_OF_HEADER");
        thread::sleep(std::time::Duration::from_secs(600));
    }
}
pub fn send_ping(stream: &mut TcpStream) {
    send_message(stream, "PING_REQUEST:::END_OF_HEADER");
}

pub fn send_message(stream: &mut TcpStream, message: &str) -> Result<()> {
    stream.write_all(message.as_bytes())
}

pub fn process_small_ping_request_response(stream: &mut TcpStream, buffer: &str) {
    println!("Received small ping request response");
    let end_of_json = "END_OF_JSON";

    if buffer.contains(end_of_json) {
        let parts: Vec<&str> = buffer.split(end_of_json).collect();
        let json_content = parts[0];
        let _json_trash = parts[1];

        // Parse the JSON buffer
        let json_value: Value = serde_json::from_str(json_content).expect("Invalid JSON");

        // Extract specific values from the JSON
        let username = json_value
            .get("user")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let _device_name = json_value
            .get("device_name")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let _device_number = json_value
            .get("device_number")
            .and_then(Value::as_i64)
            .unwrap_or(0); // Defaulting to 0 if missing
        let files: Option<Vec<Files>> = json_value
            .get("files")
            .and_then(|files| files.as_array())
            .map(|files_array| {
                files_array
                    .iter()
                    .map(|file| from_value::<Files>(file.clone()).expect("Invalid file JSON"))
                    .collect()
            });

        let _date_added = json_value
            .get("date_added")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let devices = database_handler::get_devices(username).unwrap().unwrap();
        database_handler::update_devices(
            stream,
            username,
            devices,
            _device_name,
            _device_number,
            files,
            _date_added,
        )
        .unwrap();

        // TODO: If the device doesn't match any of the devices in the database, send a big ping
        // TODO: Make sure devices are updated properly
    }
}

pub fn process_ping_request_response(
    buffer: &str,
    _username: &str,
    _password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received ping request response");
    // println!("Buffer: {}", buffer);
    // println!("Username: {}", username);
    // println!("Password: {}", password);
    let end_of_json = "END_OF_JSON";

    if buffer.contains(end_of_json) {
        let parts: Vec<&str> = buffer.split(end_of_json).collect();
        let json_content = parts[0];
        let _json_trash = parts[1];

        // Parse the JSON buffer
        let json_value: Value = serde_json::from_str(json_content).expect("Invalid JSON");

        // Extract specific values from the JSON
        let username = json_value
            .get("user")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let device_number = json_value
            .get("device_number")
            .and_then(Value::as_i64)
            .unwrap_or(0); // Defaulting to 0 if missing
        let device_name = json_value
            .get("device_name")
            .and_then(Value::as_str)
            .unwrap_or_default();
        // Deserialize the files array
        let files: Option<Vec<Files>> = json_value
            .get("files")
            .and_then(|files| files.as_array())
            .map(|files_array| {
                files_array
                    .iter()
                    .map(|file| from_value::<Files>(file.clone()).expect("Invalid file JSON"))
                    .collect()
            });
        let storage_capacity_gb = json_value
            .get("storage_capacity_GB")
            .and_then(Value::as_i64)
            .unwrap_or_default();
        let date_added = json_value
            .get("date_added")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let ip_address = json_value
            .get("ip_address")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let average_network_speed = json_value
            .get("average_network_speed")
            .and_then(Value::as_i64)
            .unwrap_or_default();
        let upload_network_speed = json_value
            .get("upload_network_speed")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let download_network_speed = json_value
            .get("download_network_speed")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let gpu_usage = json_value
            .get("gpu_usage")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let cpu_usage = json_value
            .get("cpu_usage")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let ram_usage = json_value
            .get("ram_usage")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let network_reliability = json_value
            .get("network_reliability")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let average_time_online = json_value
            .get("average_time_online")
            .and_then(Value::as_f64)
            .unwrap_or_default();
        let device_priority = json_value
            .get("device_priority")
            .and_then(Value::as_i64)
            .unwrap_or_default();
        let sync_status = json_value
            .get("sync_status")
            .and_then(Value::as_bool)
            .unwrap_or_default();
        let optimization_status = json_value
            .get("optimization_status")
            .and_then(Value::as_bool)
            .unwrap_or_default();
        println!("Calling append device info");
        database_handler::append_device_info(
            username,
            device_number,
            device_name,
            files,
            storage_capacity_gb,
            date_added,
            ip_address,
            average_network_speed,
            upload_network_speed,
            download_network_speed,
            gpu_usage,
            cpu_usage,
            ram_usage,
            network_reliability,
            average_time_online,
            device_priority,
            sync_status,
            optimization_status,
        );
    }
}
