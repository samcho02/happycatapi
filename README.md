# Internet Famous Cats API
API of internet famous cats 

## Technology Stack
- **Python**
- **Uvicorn** - ASGI server to run FastAPI
- **Pydanti** - Data validation
- **MongoDB** - To store GIF metadata (title, tags, URL)
- **Local Storage** - Storing actual GIFs (or links from Giphy)

## MVP Features
- **`GET /gifs`** - Retrieve a list of all cat GIF memes  
- **`GET /gifs/{id}`** - Retrieve details of a specific cat GIF meme  
- **`POST /gifs`** - Upload a new cat GIF meme (via file upload or URL)  
- **`PUT /gifs/{id}`** - Update metadata of a specific GIF meme  
- **`DELETE /gifs/{id}`** - Delete a specific GIF meme from the collection
