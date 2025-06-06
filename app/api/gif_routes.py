from fastapi import APIRouter, HTTPException
from app.db.gifs_test_db import gifs_test_db
from app.core.utils import gif_service

router = APIRouter()
gif_service = gif_service(gifs_test_db)

# get all gifs in the test db
@router.get("/")
async def get_all_gifs():
    return gif_service.get_all_gifs()

# get random gif
@router.get("/random")
async def get_random_gif():
    return gif_service.get_random_gif()

# get gif by tag
@router.get("/{tag}")
async def get_gif_by_tag(tag: str):
    gif = gif_service.search_by_tag(tag)

    if not gif:
        raise HTTPException(status_code=404, detail="GIF not found") 
    
    return gif