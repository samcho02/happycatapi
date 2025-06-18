import random
from fastapi import Request, HTTPException
from app.schemas.gifs import *
from pymongo.collection import Collection
from app.schemas.gifs import GIFcollection, GIFmodel
from app.db.gifs_db import gifs_collection

class gif_new_service:
    """
    Service class for managing cat gif data.
        
    All business logic for fetching data from the database.
    """
    
    async def get_all_gifs(self):
        """
        Returns all gifs in database.

        Returns:
            GIFcollection: contains all GIF items
        """
        
        return GIFcollection(gifs=await gifs_collection.find())
    
    async def get_random_gif(self):
        """
        Returns a random gif item.

        Returns:
            GIFmodel : a random choice of GIF
        """
    
        return await gifs_collection.aggregate([{"$sample": {"size": 1}}])
    
    async def search_by_name(self, name: str):
        """
        Searches for the gif with corresponding tag in database.

        Args:
            name (str): The name to search for. 
        
        Returns:
            GIFmodel: corresponding GIF item.
        
        Raises:
            HTTPException: Status code 404 (Not found) if none found.  
        """
        
        if result := await gifs_collection.find_one({"name":name}):
            return result
        
        raise HTTPException(
            status_code=404,
            detail=f'GIF with name "{name}" not found'
        )
        
    async def search_by_tag(self, tag: str):
        """
        Searches for the gifs with corresponding tag in database.

        Args:
            tag (str): The tag to search for. 
        
        Returns:
            GIFcollection: corresponding dictionary value.
        
        Raises:
            HTTPException: Status code 404 (Not found) if none found.
        """

        if result := await gifs_collection.find({"tags": {"$in": [tag]}}):
            return GIFcollection(gifs=result)
        
        raise HTTPException(
            status_code=404,
            detail=f'GIF with tag "{tag}" not found'
        )
    
    def check_header(self, request:Request, accepted:str):
        """Check if header includes acceptable media type.
        If request includes header, it must be same as accepted or */* (any).

        Args:
            request (Request): incoming HTTP request
            accepted (str): accepted media type

        Raises:
            HTTPException: Status code 406 (Not acceptable) if 
        """
    
        header = request.headers.get("accept")
        if header and accepted not in header and "*/*" not in header:
            raise HTTPException(
                status_code=406,
                detail=(
                    f'Not Acceptable: Accept header "{header}" is not supported. '
                    f'Only "{accepted}" is allowed.'
                )
            )
  
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
            db (GIFcollection): database storing all GIFs.
            # collection (MongoDB Collection): Collection of GIF documents.
        """
        
        self.db = db
        self.name_map = {}
        self.tag_map = {}
        
        for gif_item in db.gifs:
            self.name_map[gif_item.name] = gif_item
            
            for tag in gif_item.tag:
                if tag not in self.tag_map:
                    self.tag_map[tag] = GIFcollection(gifs=[])
                    
                self.tag_map[tag].gifs.append(gif_item)
        
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
        Returns a random gif item.

        Returns:
            dict: Random choice of dictionary. 
            # (Cursor) : MongoDB Cursor to a random choice of GIF. 
        """
        
        # return random.choice(list(self.db.values()))
        
        random_idx = random.randint(0, len(self.db.gifs)-1)
        return self.db.gifs[random_idx]
    
        # return self.collection.aggregate([{"$sample": {"size": 1}}])
    
    def search_by_name(self, name: str):
        """
        Searches for the gif with corresponding tag in database.

        Args:
            name (str): The name to search for. 
        
        Returns:
            GIFmodel with the corresponding name.
            # gif (Cursor): MongoDB Cursor corresponding GIF record.
        
        Raises:
            HTTPException: Status code 404 (Not found) if none found.  
        """
        
        # return self.db.get(tag.lower())
    
        if result := self.name_map.get(name):
            return result

        raise HTTPException(
            status_code=404,
            detail=f'GIF with name "{name}" not found'
        )
    
        # gif = await self.collection.find_one({"_id": ObjectId(id)})
        # return gif
        
    def search_by_tag(self, tag: str):
        """
        Searches for the gifs with corresponding tag in database.

        Args:
            tag (str): The tag to search for. 
        
        Returns:
            GIFcollection: corresponding dictionary value.
        
        Raises:
            HTTPException: Status code 404 (Not found) if none found.
        """
        
        # return self.db.get(tag.lower())

        if result := self.tag_map.get(tag):
            return result
        
        raise HTTPException(
            status_code=404,
            detail=f'GIF with tag "{tag}" not found'
        )
    
        # gif = await self.collection.find_one({"_id": ObjectId(id)})
        # return gif
    
    def check_header(self, request:Request, accepted:str):
        """Check if header includes acceptable media type.
        If request includes header, it must be same as accepted or */* (any).

        Args:
            request (Request): incoming HTTP request
            accepted (str): accepted media type

        Raises:
            HTTPException: Status code 406 (Not acceptable) if 
        """
    
        header = request.headers.get("accept")
        if header and accepted not in header and "*/*" not in header:
            raise HTTPException(
                status_code=406,
                detail=(
                    f'Not Acceptable: Accept header "{header}" is not supported. '
                    f'Only "{accepted}" is allowed.'
                )
            )
            
