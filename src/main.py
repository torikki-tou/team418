import os
import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.presentation_layer.handlers import router


async def main() -> None:
    API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
