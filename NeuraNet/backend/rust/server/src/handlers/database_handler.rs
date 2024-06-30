use super::ping_handler;
use futures::stream::TryStreamExt;
use mongodb::bson;
use mongodb::bson::oid::ObjectId;
use mongodb::error::Result;
use mongodb::{bson::doc, options::ClientOptions, Client, Collection};
use serde::{Deserialize, Serialize};

use std::sync::Arc;
use tokio::io::{self, split, AsyncReadExt, AsyncWriteExt, Error, WriteHalf};
use tokio::net::TcpStream;
use tokio::sync::Mutex;

#[derive(Serialize, Deserialize, Debug)]
pub struct Server {
    pub total_data_processed: i64,
    pub total_number_of_requests: i64,
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
    #[serde(default)]
    pub file_type: String,
    #[serde(default)]
    pub file_name: String,
    #[serde(default)]
    pub file_path: String,
    #[serde(default)]
    pub date_uploaded: String,
    #[serde(default)]
    pub file_size: i64,
    #[serde(default)]
    pub file_priority: i64,
    #[serde(default)]
    pub file_parent: String,
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
        format!("{:.9} TB", bytes as f64 / terabyte as f64)
    } else if bytes >= gigabyte {
        format!("{:.9} GB", bytes as f64 / gigabyte as f64)
    } else if bytes >= megabyte {
        format!("{:.9} MB", bytes as f64 / megabyte as f64)
    } else if bytes >= kilobyte {
        format!("{:.9} KB", bytes as f64 / kilobyte as f64)
    } else {
        format!("{} bytes", bytes)
    }
}

async fn get_client() -> Result<Client> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";

    let client_options = ClientOptions::parse(uri).await?;
    let client = Client::with_options(client_options)?;

    Ok(client)
}
pub async fn get_total_data_processed() -> mongodb::error::Result<Option<i64>> {
    // Use logging library instead of println! for errors

    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client_options = ClientOptions::parse(uri).await?;
    let client = Client::with_options(client_options)?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");
    let result = my_coll
        .find_one(doc! { "total_data_processed": { "$exists": true } }, None)
        .await?;

    if let Some(server_data) = result {
        println!(
            "Total Data Processed: {}",
            format_bytes(server_data.total_data_processed)
        );
        Ok(Some(server_data.total_data_processed))
    } else {
        println!("No document found with 'total_data_processed' field.");
        Ok(None)
    }
}

pub async fn get_total_requests_processed() -> Result<Option<i64>> {
    let client = get_client().await?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");
    let result = my_coll
        .find_one(
            doc! { "total_number_of_requests": { "$exists": true } },
            None,
        )
        .await?;

    if let Some(server_data) = result {
        println!(
            "Total Requests Processed: {}",
            server_data.total_number_of_requests
        );
        Ok(Some(server_data.total_number_of_requests))
    } else {
        println!("No document found with 'total_number_of_requests' field.");
        Ok(None)
    }
}

pub async fn initialize() -> Result<()> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let mut cursor = collection.find(None, None).await?;

    while let Some(result) = cursor.try_next().await? {
        let mut user = result;
        let user_id = user._id.clone();
        let mut updated = false;

        for device in &mut user.devices {
            if device.online {
                device.online = false;
                updated = true;
            }
        }

        if updated {
            collection
                .update_one(
                    doc! { "_id": user_id, "devices.online": true },
                    doc! { "$set": { "devices.$[].online": false } },
                    None,
                )
                .await?;
        }
    }

    Ok(())
}

pub async fn update_total_data_processed(bytes_read: usize) -> Result<()> {
    let client = get_client().await?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");

    let bytes_read = bytes_read as i64;
    let increment_amount = bytes_read;

    let filter = doc! { "total_data_processed": { "$exists": true } };
    let update = doc! { "$inc": { "total_data_processed": increment_amount } };

    match my_coll.find_one_and_update(filter, update, None).await {
        Ok(Some(server_data)) => {
            println!(
                "Updated Total Data Processed: {}",
                server_data.total_data_processed
            );
        }
        Ok(None) => {
            println!("No document found with 'total_data_processed' field or update failed.");
        }
        Err(e) => {
            println!("Error updating total data processed: {:?}", e);
        }
    }

    Ok(())
}

pub async fn update_number_of_requests_processed() -> mongodb::error::Result<()> {
    let client = get_client().await?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");

    let increment_amount = 1;

    let filter = doc! { "total_number_of_requests": { "$exists": true } };
    let update = doc! { "$inc": { "total_number_of_requests": increment_amount } };
    let result = my_coll.find_one_and_update(filter, update, None).await?;

    if let Some(server_data) = result {
        println!(
            "Number_of_requests: {}",
            server_data.total_number_of_requests + increment_amount
        );
    } else {
        println!("No document found with 'total_number_of_requests' field or update failed.");
    }

    Ok(())
}

pub async fn get_user(user: &str) -> mongodb::error::Result<Option<Users>> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let result = collection.find_one(doc! { "username": user }, None).await?;

    Ok(result)
}

pub async fn get_username(user: &str) -> mongodb::error::Result<Option<Users>> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let result = collection.find_one(doc! { "username": user }, None).await?;

    Ok(result)
}

pub async fn get_devices(user: &str) -> mongodb::error::Result<Option<Vec<Devices>>> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let result = collection.find_one(doc! { "username": user }, None).await?;
    let devices = result.map(|user| user.devices);
    Ok(devices)
}

pub async fn update_devices(
    stream: Arc<Mutex<WriteHalf<TcpStream>>>,
    user: &str,
    devices: Vec<Devices>,
    device_name: &str,
    device_number: i64,
    files: Option<Vec<Files>>,
    date_added: &str,
) -> mongodb::error::Result<Option<Users>> {
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let result = collection.find_one(doc! { "username": user }, None).await?;

    let files_bson = bson::to_bson(&files).map_err(|e| mongodb::error::Error::from(e))?;

    let update_doc = doc! {
        "devices.$.device_number": device_number,
        "devices.$.files": files_bson,
        "devices.$.date_added": date_added,
    };

    println!("Checking if device already exists");

    let pipeline = vec![
        doc! { "$match": { "username": user }},
        doc! { "$unwind": "$devices" },
        doc! { "$match": { "devices.device_name": device_name }},
    ];
    let device_exists = collection
        .aggregate(pipeline, None)
        .await?
        .try_next()
        .await?;

    if device_exists.is_some() {
        println!("Device already exists, updating device info");
        collection
            .update_one(
                doc! { "username": user, "devices.device_name": device_name },
                doc! { "$set": update_doc },
                None,
            )
            .await?;
    } else {
        println!("Device does not exist, sending a big ping");
        ping_handler::send_ping(stream);
    }
    Ok(result)
}

pub async fn append_device_info(
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
    let client = get_client().await?;
    let collection: Collection<Users> = client.database("myDatabase").collection("users-dev");

    let files_bson = bson::to_bson(&files).map_err(|e| mongodb::error::Error::from(e))?;

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

    let pipeline = vec![
        doc! { "$match": { "username": user }},
        doc! { "$unwind": "$devices" },
        doc! { "$match": { "devices.device_name": device_name }},
    ];
    let device_exists = collection
        .aggregate(pipeline, None)
        .await?
        .try_next()
        .await?;

    if device_exists.is_some() {
        println!("Device already exists, updating device info");
        collection
            .update_one(
                doc! { "username": user, "devices.device_name": device_name },
                doc! { "$set": update_doc },
                None,
            )
            .await?;
        collection
            .update_one(
                doc! { "username": user, "devices.device_name": device_name },
                doc! { "$push": {
                    "devices.$.upload_network_speed": upload_network_speed,
                    "devices.$.download_network_speed": download_network_speed,
                    "devices.$.gpu_usage": gpu_usage,
                    "devices.$.cpu_usage": cpu_usage,
                    "devices.$.ram_usage": ram_usage,
                }},
                None,
            )
            .await?;
    } else {
        println!("Device does not exist, appending device info");
        let device_doc = doc! {
            "device_name": device_name,
            "device_number": device_number,
            "files": files_bson,
            "storage_capacity_gb": storage_capacity_gb,
            "date_added": date_added,
            "ip_address": ip_address,
            "avg_network_speed": avg_network_speed,
            "upload_network_speed": vec![upload_network_speed],
            "download_network_speed": vec![download_network_speed],
            "gpu_usage": vec![gpu_usage],
            "cpu_usage": vec![cpu_usage],
            "ram_usage": vec![ram_usage],
            "network_reliability": network_reliability,
            "average_time_online": average_time_online,
            "device_priority": device_priority,
            "sync_status": sync_status,
            "optimization_status": optimization_status,
            "online": true,
        };
        collection
            .update_one(
                doc! { "username": user },
                doc! { "$push": { "devices": device_doc }},
                None,
            )
            .await?;
    }

    Ok(None)
}
