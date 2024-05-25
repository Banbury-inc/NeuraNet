use futures::stream::Any;
use mongodb::bson;
use mongodb::bson::oid::ObjectId;
use mongodb::{
    bson::doc,
    bson::to_bson,
    bson::Bson,
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
    username: String,
    first_name: String,
    last_name: String,
    phone_number: String,
    email: String,
    devices: Vec<Devices>,
}
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Devices {
    device_name: String,
    device_number: i64,
    // files: Vec<Files>,
    date_added: String,
    online: bool,
}
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Files {
    file_name: String,
    date_uploaded: String,
    file_size: i64,
}

pub fn get_total_data_processed() -> mongodb::error::Result<()> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let client = Client::with_uri_str(uri)?;
    let my_coll: Collection<Server> = client.database("myDatabase").collection("server");
    let result = my_coll.find_one(doc! { "total_data_processed": { "$exists": true } }, None)?;

    if let Some(server_data) = result {
        println!("Total Data Processed: {}", server_data.total_data_processed);
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
