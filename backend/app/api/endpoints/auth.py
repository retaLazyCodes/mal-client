import secrets
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import httpx
from app.core.config import get_settings
from app.core.security import generate_code_verifier, generate_code_challenge
from app.core.database import SessionLocal

router = APIRouter()
settings = get_settings()

# In-memory store for code verifiers (for demonstration)
# In production, use Redis or a secure cookie/session
code_verifiers = {}

@router.get("/login")
def login():
    """
    Redirects the user to MyAnimeList's authorization page.
    """
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Store verifier to use later in /callback
    state = secrets.token_urlsafe(16)
    code_verifiers[state] = code_verifier

    params = {
        "response_type": "code",
        "client_id": settings.MAL_CLIENT_ID,
        "code_challenge": code_challenge,
        "state": state,
        "redirect_uri": settings.MAL_CALLBACK_URL,
    }
    
    auth_url = "https://myanimelist.net/v1/oauth2/authorize"
    query_params = "&".join([f"{k}={v}" for k, v in params.items()])
    
    return RedirectResponse(f"{auth_url}?{query_params}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/callback")
async def callback(code: str, state: str, db: Session = Depends(get_db)):
    """
    Handles the redirect from MAL, exchanges code for tokens, and creates/updates user.
    """
    # 1. Validate state and get code_verifier
    code_verifier = code_verifiers.get(state)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    # Remove from store once used
    del code_verifiers[state]

    # 2. Exchange code for tokens
    token_url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": settings.MAL_CLIENT_ID,
        "client_secret": settings.MAL_CLIENT_SECRET,
        "code": code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": settings.MAL_CALLBACK_URL,
    }
    
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=data)
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to get tokens: {token_response.text}")
        
        tokens = token_response.json()
        
        # 3. Get user info from MAL to identify the user
        user_info_response = await client.get(
            "https://api.myanimelist.net/v2/users/@me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        if user_info_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info from MAL")
        
        user_info = user_info_response.json()
        mal_id = user_info["id"]
        username = user_info["name"]

        # 4. Create or update user in our database
        from app.models.user import User
        user = db.query(User).filter(User.mal_id == mal_id).first()
        
        if not user:
            user = User(mal_id=mal_id, username=username)
            db.add(user)
        
        user.access_token = tokens["access_token"]
        user.refresh_token = tokens["refresh_token"]
        user.token_expires_in = tokens["expires_in"]
        
        db.commit()
        db.refresh(user)

    return {
        "message": "Authenticated successfully",
        "user": {
            "id": user.id,
            "mal_id": user.mal_id,
            "username": user.username
        }
    }
