from fastapi import APIRouter, Request, HTTPException
from app.db.gifs_test_db import gifs_test_db
from app.core.utils import gif_service
from app.schemas.gifs import *

router = APIRouter()
service = gif_service(gifs_test_db)

# get all gifs in the test db
@router.get("/",
    response_description="List all GIFs",
    response_model=GIFcollection,
    response_model_by_alias=False,
)
async def get_all_gifs(request: Request):
    service.check_header(request, "application/json")
    return service.get_all_gifs()


# get random gif
# TODO: return as image/gif?
@router.get("/random",
    response_description="Get a random GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_random_gif(request:Request):
    service.check_header(request, "application/json")
    return service.get_random_gif()


# get gif by name
# TODO: return as image/gif?
@router.get("/{name}",
    response_description="Get a single GIF",
    response_model=GIFmodel,
    response_model_by_alias=False,
)
async def get_gif_by_name(name: str, request: Request):
    service.check_header(request, "application/json")
    
    if not (gif := service.search_by_name(name)):
        raise HTTPException(status_code=404, detail=f'GIF with name "{name}" not found') 
    
    return gif