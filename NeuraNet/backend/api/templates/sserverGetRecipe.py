import pymongo
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder data with your Atlas connection string. Be sure it includes
# a valid username and password! Note that in a production environment,
# you should not store your password in plain-text here.

uri = "mongodb+srv://mmills6060:Dirtballer6060@banbury.fx0xcqk.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
try:
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

# Use a database named "myDatabase"
db = client.myDatabase

# Use a collection named "recipes"
my_collection = db["recipes"]

# FIND DOCUMENTS
#
# To retrieve all of the data in a collection, call find() with an empty filter. 

result = my_collection.find()

if result:    
    for doc in result:
        my_recipe = doc['name']
        my_ingredient_count = len(doc['ingredients'])
        my_prep_time = doc['prep_time']
        print("%s has %d ingredients and takes %d minutes to make." % (my_recipe, my_ingredient_count, my_prep_time))
else:
    print("No documents found.")

print("\n")

# You can also find a single document. Let's find a document
# that has the string "potato" in the ingredients list.

my_doc = my_collection.find_one({"ingredients": "potato"})

if my_doc is not None:
    print("A recipe which uses potato:")
    print(my_doc)
else:
    print("I didn't find any recipes that contain 'potato' as an ingredient.")
print("\n")
