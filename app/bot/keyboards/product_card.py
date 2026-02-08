from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def product_card_keyboard(category_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад к товарам",
                    callback_data=f"cat_{category_id}"
                )
            ]
        ]
    )
