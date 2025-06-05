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
    return """^>⩊<^ Welcome to the Happy Cat API ^>⩊<^

    This API delivers GIFs of world-renowned cats — here to brighten your day.  
    Co-authored by Sujin Shin and Sungmin Cho.

    Available endpoints:
    GET /gifs           - Retrieve a list of all cat GIF memes  
    GET /gifs/{id}      - Retrieve details of a specific cat GIF meme  
    """


@app.get("/happycat")
def get_happy_cat():
    return {
        "catID": 0, 
        "alias": "happycat", 
        "url": "https://tenor.com/bXAn9.gif"
    }
    # return Item(0, "happycat", "https://tenor.com/bXAn9.gif")
