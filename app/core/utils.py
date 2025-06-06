from fastapi import HTTPException
import random

class gif_service:
    """
    Service class for managing cat gif data.
        
    All business logic for fetching data from the database.
    """
    def __init__(self, db: dict={}):
        """
        Initialize service class with database.

        Args:
            db (dict): Dictionary representing GIF database.
        """
        self.db = db

    def get_all_gifs(self):
        """
        Returns all gifs in database.

        Returns:
            dict: All database (dict withint dict).
        """
        return self.db.values()
    
    def get_random_gif(self):
        """
        Returns a random gif's primary key.

        Returns:
            dict: Random choice of dictionary. 
        """
        return random.choice(list(self.db.values()))
    
    def search_by_tag(self, tag: str):
        """
        Searches for the gif with corresponding tag in database.

        Args:
            tag (str): The tag to search for. 
        
        Returns:
            dict: Corresponding dictionary value, 
                  None if the tag does not exist.
            
        """
        return self.db.get(tag.lower())