from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📦 Каталог")
async def catalog(message: Message):
    await message.answer("📦 Каталог в разработке 💎")


@router.message(F.text == "ℹ️ О магазине")
async def about(message: Message):
    await message.answer(
        "ℹ️ MONOSTONE\n\n"
        "Ювелирные украшения высокого качества."
    )


@router.message(F.text == "📞 Контакты")
async def contacts(message: Message):
    await message.answer(
        "📞 Контакты\n\n"
        "Telegram: @monostone"
    )
