from aiogram import Router
from aiogram.types import CallbackQuery

from sqlalchemy import select

from app.db.engine import AsyncSessionLocal
from app.db.models.product import Product
from app.bot.keyboards.product import products_keyboard

router = Router()


@router.callback_query(lambda c: c.data.startswith("product_"))
async def product_card(callback: CallbackQuery):
    product_id = int(callback.data.replace("product_", ""))

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()

    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return

    text = (
        f"💍 <b>{product.name}</b>\n\n"
        f"💰 <b>Цена:</b> {product.price} ₽\n\n"
    )

    if product.description:
        text += f"{product.description}\n\n"

    text += (
        f"⚖️ <b>Вес:</b> {product.weight or '—'}\n"
        f"📏 <b>Размер:</b> {product.size or '—'}\n"
        f"💎 <b>Вставки:</b> {product.inserts or '—'}\n"
        f"🔩 <b>Металл:</b> {product.metal or '—'}\n"
        f"🏷 <b>УИН:</b> {product.uin or '—'}"
    )

    await callback.answer()

    await callback.message.answer_photo(
        photo=product.photo,
        caption=text,
        parse_mode="HTML"
    )
