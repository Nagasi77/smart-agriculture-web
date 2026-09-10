from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.services.auth import decode_access_token

# Skema Header untuk IoT API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Skema Bearer Token untuk Operator Dasbor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def verify_iot_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Middleware/Dependency keamanan khusus IoT:
    Memeriksa header X-API-Key dari paket data masuk fisik.
    """
    if not api_key or api_key != settings.IOT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Akses Ditolak: API Key IoT tidak valid.",
        )
    return api_key


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Middleware/Dependency keamanan khusus Operator Dasbor:
    Memvalidasi JWT Bearer token dan mengambil entitas user aktif dari database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sesi tidak valid atau telah kedaluwarsa. Silakan login kembali.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Cari user di database
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
