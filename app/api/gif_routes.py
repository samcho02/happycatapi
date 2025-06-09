from fastapi import APIRouter, HTTPException
from app.db.gifs_test_db import gifs_test_db
from app.core.utils import gif_service
from app.schemas.gifs import *

router = APIRouter()
gif_service = gif_service(gifs_test_db)

# get all gifs in the test db
@router.get("/",
    response_description="List all GIFs",
    response_model=GIFcollection,
    response_model_by_alias=False,
)
async def get_all_gifs():
    return gif_service.get_all_gifs()


# get random gif
@router.get("/random",
    response_description="Get a random GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_random_gif():
    return gif_service.get_random_gif()


# get gif by tag
@router.get("/{tag}",
    response_description="Get a single GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_gif_by_name(name: str):
    if (
        gif := gif_service.search_by_name(name)
    ) is not None:
        return gif

    raise HTTPException(status_code=404, detail="GIF named {} not found") 