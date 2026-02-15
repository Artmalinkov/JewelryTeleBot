#!/usr/bin/env python3
"""
Тестовый бот на aiogram 3.x (исправленная версия)
"""
import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold, hcode, hlink, hitalic, hunderline
from aiogram.client.default import DefaultBotProperties

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем токен
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("❌ Токен не найден!")
    exit(1)

# Инициализация бота с правильным parse_mode
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Хранилище в памяти
user_stats = {}
messages_count = 0


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    user = message.from_user
    user_id = user.id

    # Обновляем статистику
    if user_id not in user_stats:
        user_stats[user_id] = {
            'first_seen': datetime.now(),
            'username': user.username,
            'first_name': user.first_name,
            'commands_count': 0
        }

    user_stats[user_id]['commands_count'] += 1

    # ✅ ИСПРАВЛЕНО: убраны все возможные проблемные теги
    welcome_text = (
        f"{hbold('👋 Привет, ' + user.first_name + '!')}\n\n"
        f"✅ Тестовый бот на aiogram 3.x успешно запущен!\n"
        f"🖥️ Сервер: TimeWeb\n"
        f"⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        f"{hbold('📋 Доступные команды:')}\n"
        f"• /start - начать работу\n"
        f"• /help - помощь\n"
        f"• /stats - статистика\n"
        f"• /info - информация\n"
        f"• /echo текст - повторить текст\n"
        f"• /test - тест форматирования\n\n"
        f"Просто отправьте любое сообщение - я его повторю!"
    )

    await message.answer(welcome_text)
    logger.info(f"Пользователь {user_id} запустил бота")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """Обработчик команды /help"""
    help_text = (
        f"{hbold('📚 Справка по боту')}\n\n"
        f"Команды:\n"
        f"• /start - начало работы\n"
        f"• /help - эта справка\n"
        f"• /stats - статистика\n"
        f"• /info - информация\n"
        f"• /echo текст - повторить текст\n"
        f"• /test - тест форматирования\n\n"
        f"Статус:\n"
        f"• Бот: работает\n"
        f"• База данных: отключена\n"
        f"• Режим: тестовый"
    )

    await message.answer(help_text)


@dp.message(Command("stats"))
async def command_stats_handler(message: Message) -> None:
    """Обработчик команды /stats"""
    global messages_count

    total_users = len(user_stats)
    total_commands = sum(u['commands_count'] for u in user_stats.values())

    stats_text = (
        f"{hbold('📊 Статистика бота')}\n\n"
        f"👥 Всего пользователей: {total_users}\n"
        f"💬 Всего сообщений: {messages_count}\n"
        f"⚡ Команд выполнено: {total_commands}\n"
        f"💾 Режим: память (RAM)\n\n"
        f"⏰ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
    )

    await message.answer(stats_text)


@dp.message(Command("info"))
async def command_info_handler(message: Message) -> None:
    """Обработчик команды /info"""
    import platform

    info_text = (
        f"{hbold('🖥️ Информация о сервере')}\n\n"
        f"• Хостинг: TimeWeb Cloud\n"
        f"• ОС: {platform.system()} {platform.release()}\n"
        f"• Python: {platform.python_version()}\n"
        f"• aiogram: 3.x\n\n"
        f"Статус:\n"
        f"• Бот: онлайн\n"
        f"• База данных: отключена\n"
        f"• Пользователей: {len(user_stats)}"
    )

    await message.answer(info_text)


@dp.message(Command("echo"))
async def command_echo_handler(message: Message) -> None:
    """Обработчик команды /echo"""
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer(
            "❌ Укажите текст для повтора!\n"
            "Пример: /echo Привет мир"
        )
        return

    text_to_echo = args[1]
    await message.answer(f"🔊 Эхо: {text_to_echo}")


@dp.message(Command("test"))
async def command_test_handler(message: Message) -> None:
    """Обработчик команды /test"""
    test_text = (
        f"{hbold('Тест форматирования')}\n\n"
        f"{hbold('Жирный текст')}\n"
        f"{hitalic('Курсив')}\n"
        f"{hunderline('Подчеркнутый')}\n"
        f"{hcode('Моноширинный текст')}\n"
        f"Обычный текст с {hlink('ссылкой', 'https://timeweb.com')}"
    )

    await message.answer(test_text)


@dp.message(F.text)
async def echo_handler(message: Message) -> None:
    """Обработчик текстовых сообщений"""
    global messages_count
    messages_count += 1

    user = message.from_user
    text = message.text

    # Обновляем статистику если пользователь новый
    if user.id not in user_stats:
        user_stats[user.id] = {
            'first_seen': datetime.now(),
            'username': user.username,
            'first_name': user.first_name,
            'commands_count': 0
        }

    await message.answer(
        f"📝 Вы написали: {text[:100]}{'...' if len(text) > 100 else ''}"
    )


@dp.message()
async def handle_other(message: Message) -> None:
    """Обработчик других типов сообщений"""
    await message.answer(
        "ℹ️ Бот пока умеет обрабатывать только текст"
    )


async def on_startup() -> None:
    """Действия при запуске"""
    me = await bot.get_me()
    logger.info(f"🤖 Бот @{me.username} запускается...")
    print("\n" + "=" * 50)
    print("✅ ТЕСТОВЫЙ БОТ НА AIOGRAM")
    print("=" * 50)
    print(f"⏰ Время запуска: {datetime.now()}")
    print(f"🤖 Бот: @{me.username}")
    print(f"🆔 ID: {me.id}")
    print("=" * 50)
    print("📝 Для остановки: Ctrl+C")
    print("=" * 50)


async def on_shutdown() -> None:
    """Действия при остановке"""
    logger.info("🛑 Бот останавливается...")
    await bot.session.close()


async def main() -> None:
    """Главная функция"""
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")