from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse

# Create FastAPI app
app = FastAPI(
    title='Happy Cat API', 
    description='A simple API for internet famous cats!',
    version="1.0.0"
)

# class Item(BaseModel):
#     catID: int = None
#     alias: str = None
#     url:   str = None
    

'''
    GET /: Welcome endpoint
'''
@app.get("/", response_class=PlainTextResponse)
def root():
    return """^>⩊<^ Welcome to Happy Cat API ^>⩊<^
This API directs you to the GIF of world-widely renowned cats
there to make your day.

Available methods:
GET /gifs - Retrieve a list of all cat GIF memes  
GET /gifs/{id} - Retrieve details of a specific cat GIF meme  
PUT /gifs/{id} - Update metadata of a specific GIF meme  
DELETE /gifs/{id} - Delete a specific GIF meme from the collection
"""


@app.get("/happycat")
def get_happy_cat():
    return {
        "catID": 0, 
        "alias": "happycat", 
        "url": "https://tenor.com/bXAn9.gif"
    }
    # return Item(0, "happycat", "https://tenor.com/bXAn9.gif")


# class Item(BaseModel):
#     text: str = None
#     is_done: bool = False

# items = []

# @app.get("/")
# def root():
#     return {"Hello": "Giyami"}

# @app.post("/items")
# def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get("/items")
# def get_all() -> list[Item]:
#     return items

# @app.get("/items/{item_id}")
# def get_item(item_id: int) -> Item:
#     if item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

