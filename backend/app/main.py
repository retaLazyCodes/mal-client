from fastapi import FastAPI

app = FastAPI(title="MyAnimeList Custom Client")

@app.get("/")
def read_root():
    return {"message": "Welcome to MAL Custom Client API"}
