from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from sqlalchemy import select

from app.db.engine import AsyncSessionLocal
from app.bot.keyboards.catalog import categories_keyboard
from app.bot.keyboards.product import products_keyboard
from app.db.models.product import Product


router = Router()


@router.message(lambda m: m.text == "📦 Каталог")
async def catalog_handler(message: Message):
    async with AsyncSessionLocal() as session:
        keyboard = await categories_keyboard(session)

    await message.answer(
        "📦 Каталог украшений\n\nВыберите категорию:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("cat_"))
async def category_selected(callback: CallbackQuery):
    category_id = int(callback.data.replace("cat_", ""))

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        products = result.scalars().all()

    await callback.answer()

    if not products:
        await callback.message.answer("В этой категории пока нет товаров 💔")
        return

    await callback.message.answer("💍 Украшения в категории:")

    for product in products:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"{product.name} — {product.price} ₽",
                        callback_data=f"product_{product.id}"
                    )
                ]
            ]
        )

        await callback.message.answer_photo(
            photo=product.photo,
            reply_markup=keyboard
        )


@router.callback_query(lambda c: c.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        keyboard = await categories_keyboard(session)

    await callback.answer()

    await callback.message.answer(
        "📦 Каталог украшений\n\nВыберите категорию:",
        reply_markup=keyboard
    )
