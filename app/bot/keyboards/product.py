from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.product import Product


async def products_keyboard(
    session: AsyncSession,
    category_id: int
) -> InlineKeyboardMarkup:
    result = await session.execute(
        select(Product).where(Product.category_id == category_id)
    )
    products = result.scalars().all()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for product in products:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=product.name,
                callback_data=f"product_{product.id}"
            )
        ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад к категориям",
            callback_data="back_to_categories"
        )
    ])

    return keyboard
