from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.services.auth import get_password_hash


async def seed_default_admin(session: AsyncSession):
    """Pastikan setidaknya ada satu akun admin default untuk operator dasbor."""
    result = await session.execute(select(User).where(User.username == "admin"))
    admin = result.scalar_one_or_none()

    if not admin:
        default_admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role="admin",
        )
        session.add(default_admin)
        await session.commit()
        print("[SEEDER] Berhasil membuat akun default: username='admin', password='admin123'")
