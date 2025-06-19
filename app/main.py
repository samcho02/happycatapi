from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import PlainTextResponse
from app.api.gif_routes import router as gif_router
from app.core.constants import welcome_msg

# Create FastAPI app
app = FastAPI(
    title='Happy Cat API', 
    description='A simple API for internet famous cats!',
    version="1.0.0"
)

# Router for /gifs routes
app.include_router(gif_router, prefix="/gifs")

# Welcome endpoint
@app.get("/", response_class=PlainTextResponse)
async def root(request: Request):
    # If request includes header, it must be text/plain or */* (any)
    accept = request.headers.get("accept")
    if accept and "text/plain" not in accept and "*/*" not in accept:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail=(
                f'Not Acceptable: Accept header "{accept}" is not supported. '
                'Only "application/json" is allowed.')
        )
    
    return welcome_msg

