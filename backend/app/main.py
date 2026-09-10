from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings, UPLOAD_PATH
from app.database import engine, Base, AsyncSessionLocal
from app.services.seeder import seed_default_admin
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inisialisasi tabel database saat startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Jalankan seeder akun default operator
    async with AsyncSessionLocal() as session:
        await seed_default_admin(session)

    yield

    # Cleanup saat shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve berkas fisik gambar secara statis
app.mount("/static/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

# Registrasi Router
app.include_router(auth.router, prefix="/api/auth", tags=["Autentikasi Operator"])


@app.get("/api/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "storage_ready": UPLOAD_PATH.exists(),
    }
