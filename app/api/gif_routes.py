from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

gifs_test_db = {
    "happycat": {
        "id": "0",
        "url": "https://tenor.com/bXAn9.gif"
    },
    "carla": {
        "id": "1",
        "url": "https://tenor.com/rJ4PNMf6dC5.gif"
    },
    "ripcarla": {
        "id": "2",
        "url": "https://tenor.com/b78eKUM95k3.gif"
    },
    "huhcat": {
        "id": "3",
        "url": "https://tenor.com/sqMU1WMDcgD.gif"
    }
}

# get all gifs in the test db
@router.get("/")
async def get_all_gifs():
    return list(gifs_test_db.values())

# get random gif
@router.get("/random")
async def get_random_gif():
    return random.choice(list(gifs_test_db.values()))

# get gif by tag
@router.get("/{tag}")
async def get_gif_by_tag(tag: str):
    gif = gifs_test_db.get(tag.lower())

    if not gif:  # no gif of the tag
        raise HTTPException(status_code=404, detail="GIF not found") 
    
    return gif 