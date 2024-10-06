from fastapi import FastAPI
from bot import start_bot
import threading
import uvicorn
import os
from contextlib import asynccontextmanager

# Define startup event


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    # Yield control back to FastAPI
    yield


# Make a fast api app
app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Server is running and bot is alive!"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use environment variable PORT if available
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info", reload=True)
