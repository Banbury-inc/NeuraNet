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
struct Server {
    total_data_processed: i64,
}
#[derive(Serialize, Deserialize, Debug)]
struct Users {
    _id: ObjectId,
    username: String,
    first_name: String,
    last_name: String,
    phone_number: String,
    email: String,
    devices: Vec<Devices>,
}
#[derive(Serialize, Deserialize, Debug, Clone)]
struct Devices {
    device_name: String,
    online: bool,
}

pub fn update_total_data_processed() -> mongodb::error::Result<()> {
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
