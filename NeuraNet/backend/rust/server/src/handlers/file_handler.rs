pub fn process_file(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}

pub fn process_file_request(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}

pub fn process_file_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
pub fn process_file_delete_request(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file delete request");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
pub fn process_file_delete_request_response(
    buffer: &str,
    username: &str,
    password: &str,
    _file_name: &str,
    _device_name: &str,
    _file_size: &str,
) {
    println!("Received file delete request response");
    println!("Buffer: {}", buffer);
    println!("Username: {}", username);
    println!("Password: {}", password);
}
