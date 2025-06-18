import random
from fastapi import Request, HTTPException
from app.schemas.gifs import *
from pymongo.collection import Collection
from app.schemas.gifs import GIFcollection, GIFmodel


class gif_service:
    """
    Service class for managing cat gif data.
        
    All business logic for fetching data from the database.
    """
    # def __init__(self, db: dict={}):
    def __init__(self, db: GIFcollection):
    # def __init__(self, collection: Collection):
        """
        Initialize service class with database.

        Args:
            db (dict): Dictionary representing GIF database.
            # collection (MongoDB Collection): Collection of GIF documents.
        """
        self.db = db
        
        self.name_dict = {}
        
        for gif_item in db.gifs:
            self.name_dict[gif_item.name] = gif_item
        # self.collection : Collection[GIFmodel] = collection

    def get_all_gifs(self):
        """
        Returns all gifs in database.
        # The response is unpaginated and limited to 1000 results.
        # TODO - Use skip and limit parameters instead of batch size

        Returns:
            dict: All database (dict withint dict).
        #     (Cursor) : MongoDB Cursor to all GIF records
        """
        # return list(self.db.values())
        
        return self.db
        
        # gifs = await self.collection.find().to_list(1000)
        # return GIFcollection(gifs)
    
    def get_random_gif(self):
        """
        Returns a random gif's primary key.

        Returns:
            dict: Random choice of dictionary. 
            # (Cursor) : MongoDB Cursor to a random choice of GIF. 
        """
        # return random.choice(list(self.db.values()))
        
        random_idx = random.randint(0, len(self.db.gifs)-1)
        return self.db.gifs[random_idx]
    
        # return self.collection.aggregate([{"$sample": {"size": 1}}])
    
    # def search_by_tag(self, tag: str):
    def search_by_name(self, name: str):
        """
        Searches for the gif with corresponding tag in database.

        Args:
            tag (str): The tag to search for. 
            # name (str): The name to search for. 
        
        Returns:
            dict: Corresponding dictionary value, 
                  None if the tag does not exist.
            # gif (Cursor): MongoDB Cursor corresponding GIF record. 
            
        """
        # return self.db.get(tag.lower())
    
        return self.name_dict.get(name)
    
        # gif = await self.collection.find_one({"_id": ObjectId(id)})
        # return gif
    
    def check_header(self, request:Request, accepted:str):
    # If request includes header, it must be text/plain or */* (any)
        header = request.headers.get("accept")
        if header and accepted not in header and "*/*" not in header:
            raise HTTPException(
                status_code=406,
                detail=(
                    f'Not Acceptable: Accept header "{header}" is not supported. '
                    f'Only "{accepted}" is allowed.'
                )
            )
            
