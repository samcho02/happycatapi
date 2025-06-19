from fastapi import Request, HTTPException, Response, Body, status
from pymongo import ReturnDocument
from app.schemas.gifs import *
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
        return GIFcollection(gifs=await gifs_collection.find().to_list())
    
    async def get_random_gif(self):
        """
        Returns a random gif item.

        Returns:
            GIFmodel : a random choice of GIF
        """
        cursor = await gifs_collection.aggregate([{"$sample": {"size": 1}}])
        docs = await cursor.to_list(length=1)
        return GIFmodel(**docs[0])
    
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
            status_code=status.HTTP_404_NOT_FOUND,
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

        if result := await gifs_collection.find({"tag": {"$in": [tag]}}).to_list():
            return GIFcollection(gifs=result)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'GIF with tag "{tag}" not found'
        )
    
    async def add_new_gif(self, gif: GIFmodel = Body(...)):
        """
        Insert a new GIF item.
        A unique `id` will be created and provided in the response.
        """
        
        await self.check_duplicate(None, gif.name, gif.url)
                
        new_gif = await gifs_collection.insert_one(
            gif.model_dump(by_alias=True, exclude=["id"], mode="json")
        )
        created_gif = await gifs_collection.find_one(
            {"_id": new_gif.inserted_id}
        )
        
        return created_gif

    async def update_gif(self, id: str, gif: UpdateGIFmodel = Body(...)):
        """
        Update individual fields of an existing GIF item.
        Only the provided fields will be updated.
        Any missing or `null` fields will be ignored.
        """
        gif = {
            k: v for k, v in gif.model_dump(by_alias=True, mode="json").items() if v is not None
        }
        
        self.check_duplicate(id, gif.get("url"), gif.get("name"))
        
        if len(gif) >= 1:
            update_result = await gifs_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": gif},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return update_result
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GIF {id} not found")
        
        # The update is empty, but we should still return the matching document:
        if existing_student := await gifs_collection.find_one({"_id": id}):
            return existing_student
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GIF {id} not found")
    
    async def delete_gif(self, id: str):
        """
        Remove a single student record from the database.
        """
        
        delete_result = await gifs_collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"GIF {id} not found")
    
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
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=(
                    f'Not Acceptable: Accept header "{header}" is not supported. '
                    f'Only "{accepted}" is allowed.'
                )
            )
    
    def check_id(self, id: str):
        if id == "random":
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Method Not Allowed'
            )
            
        if len(id) != 24:   # ObjectId in must be a single string of 12 bytes or a string of 24 hex characters
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f'Bad request: {id} is not a valid ID.'
                )
            )
        
        try:
            int(id, 16)
        except:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f'Bad request: {id} is not a valid ID.'
                )
            )
    
    def check_body(self, body : UpdateGIFmodel | None):
        if body is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Request body required"
            )

    async def check_duplicate(self, id: str = None, name : str = None, url : str = None):
        # Ensure no name duplicates
        if name is not None:
            query = {"name":name}
            if id is not None:
                query["_id"] = {"$ne": ObjectId(id)}
            
            if (duplicate_result := await gifs_collection.find_one(query)) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Conflict: A GIF named {name} already exists."
                )

        # Ensure no url duplicates
        if url is not None:
            query = {"url":str(url)}
            if id is not None:
                query["_id"] = {"$ne": ObjectId(id)}
                
            if (duplicate_result := await gifs_collection.find_one(query)) is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Conflict: URL is tied to another GIF (id={duplicate_result['_id']})."
                )