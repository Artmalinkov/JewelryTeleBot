from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category


async def categories_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    result = await session.execute(
        select(Category)
    )
    categories = result.scalars().all()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category in categories:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"cat_{category.id}"
            )
        ])

    return keyboard
