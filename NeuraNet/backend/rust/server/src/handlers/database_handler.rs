use mongodb::bson;
use mongodb::bson::oid::ObjectId;
use mongodb::{
    bson::doc,
    sync::{Client, Collection},
};
use serde::{Deserialize, Serialize};
#[derive(Serialize, Deserialize, Debug)]
pub struct Server {
    total_data_processed: i64,
}
#[derive(Serialize, Deserialize, Debug)]
pub struct Users {
    _id: ObjectId,
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
    pub device_number: i64,
    #[serde(default)]
    pub device_name: String,
    #[serde(default)]
    pub files: Vec<Files>,
    #[serde(default)]
    pub date_added: String,
    #[serde(default)]
    pub online: bool,
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

pub fn update_devices(user: &str, devices: Vec<Devices>) -> mongodb::error::Result<Option<Users>> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users");

    let result = collection.find_one(doc! { "username": user }, None)?;

    // Convert devices to BSON before updating
    let devices_bson = bson::to_bson(&devices).map_err(|e| mongodb::error::Error::from(e))?;

    // Find the user with the specified username
    collection.update_one(
        doc! { "username": user },
        doc! { "$set": { "devices": devices_bson } },
        None,
    )?;

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
    upload_network_speed: &str,
    download_network_speed: &str,
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

    // Convert devices and files to BSON
    // let devices_bson = bson::to_bson(&devices).map_err(|e| mongodb::error::Error::from(e))?;
    let files_bson = bson::to_bson(&files).map_err(|e| mongodb::error::Error::from(e))?;

    // Create the BSON document with all the variables
    let update_doc = doc! {
        "device_name": device_name,
        "device_number": device_number,
        "files": files_bson,
        "storage_capacity_GB": storage_capacity_gb,
        "date_added": date_added,
        "ip_address": ip_address,
        "avg_network_speed": avg_network_speed,
        "upload_network_speed": upload_network_speed,
        "download_network_speed": download_network_speed,
        "gpu_usage": gpu_usage,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "network_reliability": network_reliability,
        "average_time_online": average_time_online,
        "device_priority": device_priority,
        "sync_status": sync_status,
        "online": true,
        "optimization_status": optimization_status,
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
            doc! { "$set": { "devices.$": update_doc } },
            None,
        )?;
    } else {
        // If the device does not exist, append the device info
        println!("Device does not exist, appending device info");
        collection.update_one(
            doc! { "username": user },
            doc! { "$push": { "devices": update_doc } },
            None,
        )?;
    }

    Ok(None)
}
