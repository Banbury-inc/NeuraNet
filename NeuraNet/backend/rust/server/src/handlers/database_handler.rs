use futures::stream::TryStreamExt;
use mongodb::{
    bson::doc, bson::Document, error::Result, options::ClientOptions, Client, Collection,
};

pub async fn connect_to_mongodb(
    uri: &str,
    db_name: &str,
    coll_name: &str,
) -> Result<Collection<Document>> {
    // Parse a connection string into an options struct.
    let client_options = ClientOptions::parse(uri).await?;

    // Get a handle to the deployment.
    let client = Client::with_options(client_options)?;

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
