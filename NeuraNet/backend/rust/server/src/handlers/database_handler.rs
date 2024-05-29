use super::ping_handler;
use mongodb::bson;
use mongodb::bson::oid::ObjectId;
use mongodb::{
    bson::doc,
    sync::{Client, Collection},
};
use serde::{Deserialize, Serialize};
use std::net::TcpStream;
#[derive(Serialize, Deserialize, Debug)]
pub struct Server {
    total_data_processed: i64,
}
#[derive(Serialize, Deserialize, Debug)]
pub struct Users {
    pub _id: ObjectId,
    pub username: String,
    #[serde(default)]
    pub first_name: String,
    #[serde(default)]
    pub last_name: String,
    #[serde(default)]
    pub phone_number: String,
    #[serde(default)]
    pub email: String,
    #[serde(default)]
    pub devices: Vec<Devices>,
}
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Devices {
    #[serde(default)]
    pub device_number: i64,
    #[serde(default)]
    pub device_name: String,
    #[serde(default)]
    pub files: Vec<Files>,
    #[serde(default)]
    pub storage_capacity_GB: f64,
    #[serde(default)]
    pub avg_network_speed: f64,
    #[serde(default)]
    pub usage_stats: Vec<UsageStats>,
    #[serde(default)]
    pub ip_address: String,
    #[serde(default)]
    pub date_added: String,
    #[serde(default)]
    pub online: bool,
    #[serde(default)]
    pub sync_status: bool,
    #[serde(default)]
    pub optimization_status: bool,
}
#[derive(Serialize, Deserialize, Debug, Default, Clone)]
pub struct Files {
    pub file_name: String,
    #[serde(default)]
    pub date_uploaded: String,
    #[serde(default)]
    pub file_size: i64,
    #[serde(default)]
    pub file_priority: i64,
    #[serde(default)]
    pub original_device: String,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct UsageStats {
    pub upload_network_speed: f64,
    pub download_network_speed: f64,
    pub gpu_usage: f64,
    pub cpu_usage: f64,
    pub ram_usage: f64,
    pub timestamp: String,
}

fn format_bytes(bytes: i64) -> String {
    let kilobyte = 1024;
    let megabyte = kilobyte * 1024;
    let gigabyte = megabyte * 1024;
    let terabyte = gigabyte * 1024;

    if bytes >= terabyte {
        format!("{:.2} TB", bytes as f64 / terabyte as f64)
    } else if bytes >= gigabyte {
        format!("{:.2} GB", bytes as f64 / gigabyte as f64)
    } else if bytes >= megabyte {
        format!("{:.2} MB", bytes as f64 / megabyte as f64)
    } else if bytes >= kilobyte {
        format!("{:.2} KB", bytes as f64 / kilobyte as f64)
    } else {
        format!("{} bytes", bytes)
    }
}
pub fn get_total_data_processed() -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");
    let result = my_coll.find_one(doc! { "total_data_processed": { "$exists": true } }, None)?;

    if let Some(server_data) = result {
        println!(
            "Total Data Processed: {}",
            format_bytes(server_data.total_data_processed)
        );
    } else {
        println!("No document found with 'total_data_processed' field.");
    }
    Ok(())
}

pub fn update_total_data_processed(bytes_read: usize) -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");

    // convert bytes_read to i64
    let bytes_read = bytes_read as i64;
    // Define the amount to add to 'total_data_processed'
    let increment_amount = bytes_read; // Example increment value

    // Find the document and update 'total_data_processed'
    let filter = doc! { "total_data_processed": { "$exists": true } };
    let update = doc! { "$inc": { "total_data_processed": increment_amount } };
    let result = my_coll.find_one_and_update(filter, update, None)?;

    match result {
        Some(server_data) => {
            println!(
                "Updated Total Data Processed: {}",
                server_data.total_data_processed + increment_amount
            );
        }
        None => {
            println!("No document found with 'total_data_processed' field or update failed.");
        }
    }

    Ok(())
}

pub fn initialize() -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    let cursor = collection.find(None, None)?;

    let mut docs = Vec::new();
    for result in cursor {
        let mut user = result?;
        let user_id = user._id.clone();
        let mut updated = false;

        // Iterate over devices and update their 'online' status if necessary
        for device in &mut user.devices {
            if device.online {
                device.online = false;
                updated = true;
            }
        }

        // Perform update operation if any device was updated
        if updated {
            collection.update_one(
                doc! { "_id": user_id, "devices.online": true },
                doc! { "$set": { "devices.$[].online": false } },
                None,
            )?;
        }
        docs.push(user);
    }

    Ok(())
}
pub fn get_user(user: &str) -> mongodb::error::Result<Option<Users>> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    // Find the user with the specified username
    let result = collection.find_one(doc! { "username": user }, None)?;

    Ok(result)
}
pub fn get_username(user: &str) -> mongodb::error::Result<Option<Users>> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    // Find the user with the specified username
    let result = collection.find_one(doc! { "username": user }, None)?;

    Ok(result)
}

pub fn get_devices(user: &str) -> mongodb::error::Result<Option<Vec<Devices>>> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    // Find the user with the specified username
    let result = collection.find_one(doc! { "username": user }, None)?;
    // get specifically the devices from that user
    // let devices = result.as_ref().map(|user| user.devices.clone());
    let devices = result.map(|user| user.devices);
    Ok(devices)
}

pub fn update_devices(
    stream: &mut TcpStream,
    user: &str,
    devices: Vec<Devices>,
    device_name: &str,
    device_number: i64,
    files: Option<Vec<Files>>,
    date_added: &str,
) -> mongodb::error::Result<Option<Users>> {
    // Handling a small ping response
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    let result = collection.find_one(doc! { "username": user }, None)?;

    // Convert files to BSON before updating
    let files_bson = bson::to_bson(&files).map_err(|e| mongodb::error::Error::from(e))?;

    // Create the BSON document with the fields to update
    let update_doc = doc! {
        "devices.$.device_number": device_number,
        "devices.$.files": files_bson,
        "devices.$.date_added": date_added,
    };

    println!("Checking if device already exists");

    // Use aggregation pipeline to find the specific device
    let pipeline = vec![
        doc! { "$match": { "username": user }},
        doc! { "$unwind": "$devices" },
        doc! { "$match": { "devices.device_name": device_name }},
    ];
    let device_exists = collection.aggregate(pipeline, None)?.next();

    // If the device exists, update the device info
    if let Some(_) = device_exists {
        println!("Device already exists, updating device info");
        collection.update_one(
            doc! { "username": user, "devices.device_name": device_name },
            doc! { "$set": update_doc },
            None,
        )?;
    } else {
        println!("Device does not exist, sending a big ping");
        ping_handler::send_ping(stream);
    }
    Ok(result)
}
pub fn append_device_info(
    user: &str,
    device_number: i64,
    device_name: &str,
    files: Option<Vec<Files>>,
    storage_capacity_gb: i64,
    date_added: &str,
    ip_address: &str,
    avg_network_speed: i64,
    upload_network_speed: f64,
    download_network_speed: f64,
    gpu_usage: f64,
    cpu_usage: f64,
    ram_usage: f64,
    network_reliability: f64,
    average_time_online: f64,
    device_priority: i64,
    sync_status: bool,
    optimization_status: bool,
) -> mongodb::error::Result<Option<Users>> {
    println!("Appending device info for user: {}", user);
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";

    let client = Client::with_uri_str(uri)?;

    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    // Convert files to BSON
    let files_bson = bson::to_bson(&files).map_err(|e| mongodb::error::Error::from(e))?;

    // Create the BSON document with all the variables that need to be updated
    let update_doc = doc! {
        "devices.$.device_number": device_number,
        "devices.$.files": files_bson.clone(),
        "devices.$.date_added": date_added,
        "devices.$.storage_capacity_gb": storage_capacity_gb,
        "devices.$.ip_address": ip_address,
        "devices.$.avg_network_speed": avg_network_speed,
        "devices.$.network_reliability": network_reliability,
        "devices.$.average_time_online": average_time_online,
        "devices.$.device_priority": device_priority,
        "devices.$.sync_status": sync_status,
        "devices.$.optimization_status": optimization_status,
        "devices.$.online": true,
    };

    println!("Checking if device already exists");

    // Use aggregation pipeline to find the specific device
    let pipeline = vec![
        doc! { "$match": { "username": user }},
        doc! { "$unwind": "$devices" },
        doc! { "$match": { "devices.device_name": device_name }},
    ];
    let device_exists = collection.aggregate(pipeline, None)?.next();

    // If the device exists, update the device info and append the stats to the arrays
    if let Some(_) = device_exists {
        println!("Device already exists, updating device info");
        collection.update_one(
            doc! { "username": user, "devices.device_name": device_name },
            doc! { "$set": update_doc },
            None,
        )?;
        collection.update_one(
            doc! { "username": user, "devices.device_name": device_name },
            doc! { "$push": { 
                "devices.$.upload_network_speed": upload_network_speed,
                "devices.$.download_network_speed": download_network_speed,
                "devices.$.gpu_usage": gpu_usage,
                "devices.$.cpu_usage": cpu_usage,
                "devices.$.ram_usage": ram_usage,
            }},
            None,
        )?;
    } else {
        // If the device does not exist, append the device info with initialized arrays
        println!("Device does not exist, appending device info");
        let device_doc = doc! {
            "device_name": device_name,
            "device_number": device_number,
            "files": files_bson,
            "storage_capacity_gb": storage_capacity_gb,
            "date_added": date_added,
            "ip_address": ip_address,
            "avg_network_speed": avg_network_speed,
            "upload_network_speed": vec![upload_network_speed], // Initialize with the first value
            "download_network_speed": vec![download_network_speed], // Initialize with the first value
            "gpu_usage": vec![gpu_usage], // Initialize with the first value
            "cpu_usage": vec![cpu_usage], // Initialize with the first value
            "ram_usage": vec![ram_usage], // Initialize with the first value
            "network_reliability": network_reliability,
            "average_time_online": average_time_online,
            "device_priority": device_priority,
            "sync_status": sync_status,
            "optimization_status": optimization_status,
            "online": true,
        };
        collection.update_one(
            doc! { "username": user },
            doc! { "$push": { "devices": device_doc }},
            None,
        )?;
    }

    Ok(None)
}
