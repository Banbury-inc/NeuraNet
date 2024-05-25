use super::database_handler;
use std::error::Error;
use tokio::runtime::Runtime;
pub fn call_get_some_data() -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match database_handler::get_some_data(&collection).await {
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

pub fn call_initialize() -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => match database_handler::initialize(&collection).await {
                Ok(docs) => {
                    println!("Database initialized");
                }
                Err(e) => eprintln!("Failed to retrieve documents: {}", e),
            },
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}

pub fn call_get_devices(user: &str) -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match database_handler::get_devices(&collection, user).await {
                    Ok(docs) => {
                        println!("{:?}", docs);
                    }
                    Err(e) => eprintln!("Failed to retrieve documents: {}", e),
                }
            }
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}
pub fn call_get_user() -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match database_handler::get_user(&collection, "test").await {
                    Ok(docs) => {
                        println!("{:?}", docs);
                    }
                    Err(e) => eprintln!("Failed to retrieve documents: {}", e),
                }
            }
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}
pub fn call_update_devices(username: &str, devices: &str) -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match database_handler::update_devices(&collection, username, devices).await {
                    Ok(docs) => {
                        println!("{:?}", docs);
                    }
                    Err(e) => eprintln!("Failed to retrieve documents: {}", e),
                }
            }
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}
pub fn call_update_device_numbers(username: &str) -> Result<(), Box<dyn Error>> {
    // Create a new runtime
    let rt = Runtime::new()?;

    // MongoDB URI
    let uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority";
    let db_name = "myDatabase";
    let coll_name = "users";

    // Block on the async function
    rt.block_on(async {
        // Attempt to connect to MongoDB
        match database_handler::connect_to_mongodb().await {
            Ok(collection) => {
                println!("Successfully connected to MongoDB.");
                match database_handler::update_device_numbers(&collection, username).await {
                    Ok(docs) => {
                        println!("{:?}", docs);
                    }
                    Err(e) => eprintln!("Failed to retrieve documents: {}", e),
                }
            }
            Err(e) => eprintln!("Failed to connect to MongoDB: {}", e),
        }
    });

    Ok(())
}
