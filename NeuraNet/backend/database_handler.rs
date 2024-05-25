use futures::stream::TryStreamExt;
use mongodb::{
    bson::{doc, Document},
    error::Result,
    options::ClientOptions,
    options::FindOptions,
    Client, Collection,
};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Serialize, Deserialize, Debug)]
struct Server {
    total_data_processed: i64,
}

pub async fn connect_to_mongodb(// uri: &str,
    // db_name: &str,
    // coll_name: &str,
) -> Result<Collection<Document>> {
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Parse a connection string into an options struct.
    // let client_options = ClientOptions::parse(uri).await?;

    // Get a handle to the deployment.
    // let client = Client::with_options(client_options)?;

    // Get a handle to the database and collection.
    let database = client.database(db_name);
    let collection = database.collection::<Document>(coll_name);

    Ok(collection)
}

pub async fn get_some_data(collection: &Collection<Document>) -> Result<Vec<Document>> {
    let filter = doc! {};
    let find_options = None;

    // Find the documents
    let mut cursor = collection.find(filter, find_options).await?;

    // Collect the documents
    let mut docs = Vec::new();
    while let Some(result) = cursor.try_next().await? {
        docs.push(result);
    }

    Ok(docs)
}

pub async fn initialize(collection: &Collection<Document>) -> Result<Vec<Document>> {
    let filter = doc! {};
    let find_options = None;

    // Find the documents
    let mut cursor = collection.find(filter, find_options).await?;

    // Collect the documents and update them
    let mut docs = Vec::new();
    while let Some(mut user) = cursor.try_next().await? {
        let user_id = user
            .get_object_id("_id")
            .expect("Failed to get user _id")
            .clone();

        if let Some(devices) = user.get_array_mut("devices").ok() {
            let mut updated = false;
            for device in devices.iter_mut() {
                if let Some(device_doc) = device.as_document_mut() {
                    if let Some(online) = device_doc.get_bool("online").ok() {
                        if online {
                            device_doc.insert("online", false);
                            updated = true;
                        }
                    }
                }
            }
            if updated {
                collection
                    .update_one(
                        doc! { "_id": user_id },
                        doc! { "$set": { "devices": devices.clone() } },
                        None,
                    )
                    .await?;
            }
        }
        docs.push(user);
    }

    Ok(docs)
}
pub async fn get_devices(
    collection: &Collection<Document>,
    username: &str,
) -> Result<Vec<Document>> {
    let filter = doc! { "username": username };
    let find_options = None;

    // Find the document for the given username
    let mut cursor = collection.find(filter, find_options).await?;

    // Collect the devices
    let mut devices = Vec::new();
    while let Some(user) = cursor.try_next().await? {
        if let Some(user_devices) = user.get_array("devices").ok() {
            for device in user_devices {
                if let Some(device_doc) = device.as_document() {
                    devices.push(device_doc.clone());
                }
            }
        }
    }

    Ok(devices)
}
pub async fn get_user(
    collection: &Collection<Document>,
    username: &str,
) -> Result<Option<Document>> {
    let filter = doc! { "username": username };
    let find_options = None;

    // Find the document for the given username
    let mut cursor = collection.find(filter, find_options).await?;

    // Retrieve the user document
    if let Some(user) = cursor.try_next().await? {
        return Ok(Some(user));
    }

    Ok(None)
}
pub async fn update_devices(
    collection: &Collection<Document>,
    username: &str,
    devices: &str,
) -> Result<Option<Document>> {
    let filter = doc! { "username": username };
    let find_options = None;

    // Find the document for the given username
    let mut cursor = collection.find(filter, find_options).await?;

    while let Some(mut user) = cursor.try_next().await? {
        let user_id = user
            .get_object_id("_id")
            .expect("Failed to get user _id")
            .clone();

        collection
            .update_one(
                doc! { "_id": user_id },
                doc! { "$set": { "devices": devices.clone() } },
                None,
            )
            .await?;
    }
    Ok(None)
}
// devices must be a list of the users devices and not all devices
pub async fn update_device_numbers(
    collection: &Collection<Document>,
    username: &str,
) -> Result<Option<Document>> {
    let filter = doc! { "username": username };
    let find_options = None;

    // Find the document for the given username
    let mut cursor = collection.find(filter, find_options).await?;

    if let Some(mut user) = cursor.try_next().await? {
        let user_id = user
            .get_object_id("_id")
            .expect("Failed to get user _id")
            .clone();

        if let Some(devices) = user.get_array_mut("devices").ok() {
            let mut seen_device_numbers = HashSet::new();
            let mut updated = false;

            for device in devices.iter_mut() {
                if let Some(device_doc) = device.as_document_mut() {
                    if let Some(device_number) = device_doc.get_i32("device_number").ok() {
                        if !seen_device_numbers.insert(device_number) {
                            // Device number is not unique, assign a new one
                            let new_device_number = (1..)
                                .find(|num| !seen_device_numbers.contains(num))
                                .expect("Failed to find a unique device number");
                            device_doc.insert("device_number", new_device_number);
                            seen_device_numbers.insert(new_device_number);
                            updated = true;
                        }
                    }
                }
            }

            if updated {
                collection
                    .update_one(
                        doc! { "_id": user_id },
                        doc! { "$set": { "devices": devices.clone() } },
                        None,
                    )
                    .await?;
            }
        }

        return Ok(Some(user));
    }

    Ok(None)
}
