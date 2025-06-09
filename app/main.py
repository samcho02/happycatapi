from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from app.api.gif_routes import router as gif_router

# Create FastAPI app
app = FastAPI(
    title='Happy Cat API', 
    description='A simple API for internet famous cats!',
    version="1.0.0"
)

# Router for /gifs routes
app.include_router(gif_router, prefix="/gifs")

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

