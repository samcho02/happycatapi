# Internet Famous Cats API
API of internet famous cats 

## Technology Stack
- **Python**
- **Uvicorn** - ASGI server to run FastAPI
- **Pydanti** - Data validation
- **MongoDB** - To store GIF metadata (title, tags, URL)
- **Local Storage** - Storing actual GIFs (or links from Giphy)

## MVP Features
- **`GET /gifs`** - Retrieve a list of all cat GIF meme alias 
- **`GET /gifs/random`** - Retrieve a random cat GIF meme 
- **`GET /gifs/{alias}`** - Retrieve details of a specific cat GIF meme  

**For authorized users only**
- **`POST /gifs`** - Upload a new cat GIF meme (via file upload or URL)  
- **`PUT /gifs/{id}`** - Update metadata of a specific GIF meme  
- **`DELETE /gifs/{id}`** - Delete a specific GIF meme from the collection
