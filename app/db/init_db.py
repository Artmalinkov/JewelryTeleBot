import asyncio

from app.db.engine import engine
from app.db.base import Base

from app.db.models.user import User
from app.db.models.category import Category
from app.db.models.product import Product


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
