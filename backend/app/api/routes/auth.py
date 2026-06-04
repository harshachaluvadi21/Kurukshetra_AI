"""
Authentication API routes — register, login, Google OAuth, logout, me.
"""
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.core.settings import settings
from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import (
    GoogleCallbackRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter()


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
        profile_picture=user.profile_picture,
        provider=user.provider,
        created_at=user.created_at,
    )


def _token_response(user: User) -> TokenResponse:
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=_user_response(user),
    )


# --------------------------------------------------------------------------
# POST /auth/register
# --------------------------------------------------------------------------
@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    # Validate email format (basic check)
    if "@" not in payload.email or "." not in payload.email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format",
        )

    # Check for existing user
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        name=payload.name,
        email=payload.email.lower().strip(),
        password=hash_password(payload.password),
        provider="local",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return _token_response(user)


# --------------------------------------------------------------------------
# POST /auth/login
# --------------------------------------------------------------------------
@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email.lower().strip()))
    user = result.scalar_one_or_none()

    if not user or not user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return _token_response(user)


# --------------------------------------------------------------------------
# POST /auth/google/callback
# --------------------------------------------------------------------------
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.post("/google/callback", response_model=TokenResponse)
async def google_callback(
    payload: GoogleCallbackRequest,
    db: AsyncSession = Depends(get_db),
):
    # Exchange authorization code for tokens
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": payload.code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": payload.redirect_uri,
                "grant_type": "authorization_code",
            },
        )

    if token_resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to exchange Google auth code: {token_resp.text}",
        )

    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token received from Google",
        )

    # Fetch user profile from Google
    async with httpx.AsyncClient() as client:
        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    if userinfo_resp.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch Google user profile",
        )

    google_user = userinfo_resp.json()
    email = google_user.get("email", "").lower().strip()
    name = google_user.get("name", email.split("@")[0])
    picture = google_user.get("picture")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no email",
        )

    # Find or create user
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        # Auto-create Google user
        user = User(
            name=name,
            email=email,
            password=None,
            profile_picture=picture,
            provider="google",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # Update profile picture if changed
        if picture and user.profile_picture != picture:
            user.profile_picture = picture
        if user.provider == "local":
            # Link Google to existing local account
            user.provider = "google"
        await db.commit()
        await db.refresh(user)

    return _token_response(user)


# --------------------------------------------------------------------------
# POST /auth/logout  (stateless — client removes token)
# --------------------------------------------------------------------------
@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}


# --------------------------------------------------------------------------
# GET /auth/me
# --------------------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)
