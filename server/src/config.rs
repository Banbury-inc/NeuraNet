pub const IP_ADDRESS: &str = "0.0.0.0";
pub const PORT: u16 = 443;
pub const PRINT_MESSAGE: bool = false;
pub const PRINT_HEADER: bool = false;
pub const PRINT_SEND_SMALL_PING_REQUEST: bool = false;
pub const PRINT_SEND_PING_REQUEST: bool = false;
pub const PRINT_RECEIVED_SMALL_PING_REQUEST: bool = false;
pub const PRINT_RECEIVED_PING_REQUEST: bool = false;
pub const PRINT_CHECKING_IF_DEVICE_EXISTS: bool = false;
pub const PRINT_DEVICE_EXISTS_UPDATING_INFO: bool = false;

pub fn get_bind_address() -> String {
    format!("{}:{}", IP_ADDRESS, PORT)
}

pub fn print_message() {
    if PRINT_MESSAGE {
        println!("Welcome to the Banbury NeuraNet");
    }
}
