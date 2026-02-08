from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.bot.keyboards.user import main_menu_kb
from app.db.engine import AsyncSessionLocal
from app.db.models.user import User

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, message.from_user.id)

        if not user:
            user = User(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                username=message.from_user.username,
            )
            session.add(user)
            await session.commit()

    await message.answer(
        f"Привет, {message.from_user.first_name} 👋\n"
        "Добро пожаловать в MONOSTONE 💎",
        reply_markup=main_menu_kb(),
    )
