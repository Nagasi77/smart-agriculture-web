from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Single Plant Smart Agriculture API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/smart_agriculture"

    # Security - IoT
    IOT_API_KEY: str = "super-secret-iot-static-key"

    # Security - Dashboard JWT
    JWT_SECRET: str = "super-secret-jwt-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480

    # Storage
    UPLOAD_DIR: str = "static/uploads"

    # Allowed CORS Origins
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Pastikan folder upload fisik siap digunakan
UPLOAD_PATH = Path(__file__).resolve().parent.parent / settings.UPLOAD_DIR
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
