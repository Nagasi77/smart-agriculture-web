from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserResponse
from app.services.auth import verify_password, create_access_token
from app.middleware.auth import get_current_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Login Sesi Operator Dasbor")
async def login_for_access_token(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint autentikasi operator.
    Menerima username dan password, menghasilkan access token JWT.
    """
    result = await db.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau kata sandi salah.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=UserResponse, summary="Ambil Profil Operator Aktif")
async def read_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint untuk dasbor mengecek sesi login token yang masih valid.
    """
    return current_user
