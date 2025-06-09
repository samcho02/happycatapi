import random
from fastapi import HTTPException
from app.schemas.gifs import *
from pymongo.collection import Collection

class gif_service:
    """
    Service class for managing cat gif data.
        
    All business logic for fetching data from the database.
    """
    def __init__(self, collection: dict={}):
        """
        Initialize service class with database.

        Args:
            collection (MongoDB Collection): Collection of GIF documents.
        """
        self.collection : Collection[GIFmodel] = collection

    async def get_all_gifs(self):
        """
        Returns all gifs in database.
        
        The response is unpaginated and limited to 1000 results.
        TODO - Use skip and limit parameters instead of batch size

        Returns:
            (Cursor) : MongoDB Cursor to all GIF records
        """
        
        gifs = await self.collection.find().to_list(1000)
    
        return GIFcollection(gifs)
    
    async def get_random_gif(self):
        """
        Returns a query result of random gif.

        Returns:
            (Cursor) : MongoDB Cursor to a random choice of GIF. 
        """
        return self.collection.aggregate([{"$sample": {"size": 1}}])
    
    async def search_by_name(self, name: str):
        """
        Searches for the gif with corresponding name in database.

        Args:
            name (str): The name to search for. 
        
        Returns:
            gif (Cursor): MongoDB Cursor corresponding GIF record.            
        """
        gif = await self.collection.find_one({"_id": ObjectId(id)})
        
        return gif