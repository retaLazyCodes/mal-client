from fastapi import FastAPI, Depends
from app.api.endpoints import auth_router
from app.core.config import get_settings

app = FastAPI(title="MyAnimeList Custom Client")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root(settings = Depends(get_settings)):
    return {
        "message": "Welcome to MAL Custom Client API",
        "debug_mode": settings.DEBUG,
        "mal_callback": settings.MAL_CALLBACK_URL
    }
