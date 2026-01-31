from fastapi import FastAPI, Depends
from app.config import get_settings, Settings

app = FastAPI(title="MyAnimeList Custom Client")

@app.get("/")
def read_root(settings: Settings = Depends(get_settings)):
    return {
        "message": "Welcome to MAL Custom Client API",
        "debug_mode": settings.DEBUG,
        "mal_callback": settings.MAL_CALLBACK_URL
    }
