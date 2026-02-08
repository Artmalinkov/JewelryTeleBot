from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


async def get_products_by_category(
    session: AsyncSession,
    category_id: int
) -> list[Product]:
    result = await session.execute(
        select(Product)
        .where(Product.category_id == category_id)
        .order_by(Product.id)
    )
    return result.scalars().all()
