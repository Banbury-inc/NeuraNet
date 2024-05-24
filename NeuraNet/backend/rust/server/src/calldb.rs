use super::handlers::database_handler::{connect_to_mongodb, get_some_data};
use std::error::Error;
use tokio::runtime::Runtime;

pub fn calldb() -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match connect_to_mongodb(uri, db_name, coll_name).await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match get_some_data(&collection).await {
                    Ok(docs) => {
                        println!("Retrieved documents: {:?}", docs);
                    }
                    Err(e) => eprintln!("Failed to retrieve documents: {}", e),
                }
            }
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}
