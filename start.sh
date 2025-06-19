#!/bin/bash

# Start the FastAPI server in the background
uvicorn app.main:app --host 0.0.0.0 --port $PORT &

# Run the Discord bot
python app/bot/bot.py
