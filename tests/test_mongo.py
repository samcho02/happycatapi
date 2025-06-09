from datetime import datetime   # This will be needed later
import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from a .env file:
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# Connect to your MongoDB cluster:
client = MongoClient(MONGODB_URI)

print("List all the databases in the cluster:")
for db_info in client.list_database_names():
   print(db_info)
   
   
# Get a reference to the 'sample_mflix' database:
db = client['local']

# print("List all the collections in 'admin':")
# collections = db.list_collection_names()
# for collection in collections:
#    print(collection)
   
print("List all the collections in 'local':")
collections = db.list_collection_names()
for collection in collections:
   print(collection)
   
   
# # Import the `pprint` function to print nested data:
# from pprint import pprint

# # Get a reference to the 'movies' collection:
# movies = db['movies']

# # print("Get the document with the title 'The Great Train Robbery':")
# # pprint(movies.find_one({'title': 'The Great Train Robbery'}))


# # Insert a document for the movie 'Parasite':
# insert_result = movies.insert_one({
#       "title": "Parasite",
#       "year": 2020,
#       "plot": "A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks. "
#       "But their easy life gets complicated when their deception is threatened with exposure.",
#       "released": datetime(2020, 2, 7, 0, 0, 0),
#    })

# # Save the inserted_id of the document you just created:
# parasite_id = insert_result.inserted_id
# print("_id of inserted document: {parasite_id}".format(parasite_id=parasite_id))


# import bson # <- Put this line near the start of the file if you prefer.

# # Look up the document you just created in the collection:
# print(movies.find_one({'_id': bson.ObjectId(parasite_id)}))

# # Look up the documents you've created in the collection:
# for doc in movies.find({"title": "Parasite"}):
#    pprint(doc)
   
# # Update *all* the Parasite movie docs to the correct year:
# update_result = movies.update_many({"title": "Parasite"}, {"$set": {"year": 2019}})

# # Delete all matching movie docs
# movies.delete_many(
#    {"title": "Parasite",}
# )

# # See that no movies titled Parasite are there now
# print("Search result for 'Parasite'", movies.find_one({"title": "Parasite"}))