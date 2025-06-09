import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

client = AsyncMongoClient(MONGODB_URI)

gifs_collection = client['data']['gifs']

# users = client[]