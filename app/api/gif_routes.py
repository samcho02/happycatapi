from fastapi import APIRouter, Request, HTTPException, status, Body
from app.db.gifs_test_db import gifs_test_db
from app.core.utils import gif_new_service
from app.schemas.gifs import *

router = APIRouter()
service = gif_new_service()


# ----- Public methods (GET) -----
"""Get multiple GIFs

If tag parameter is given, return all GIFs with the tags.
Otherwise, return all GIFs in the database.
"""
@router.get("/",
    response_description="Get multiple GIFs",
    response_model=GIFcollection,
    response_model_by_alias=False,
)
async def get_all_gifs(request: Request, tag: str | None = None):
    service.check_header(request, "application/json")
    
    if tag:
        return await service.search_by_tag(tag)
    
    return await service.get_all_gifs()


"""Get a random GIF"""
# TODO: return as image/gif?
@router.get("/random",
    response_description="Get a random GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_random_gif(request:Request):
    service.check_header(request, "application/json")
    return await service.get_random_gif()


"""Get a GIF by name"""
# TODO: return as image/gif?
@router.get("/{name}",
    response_description="Get a single GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_gif_by_name(name: str, request: Request):
    service.check_header(request, "application/json")
    return await service.search_by_name(name)