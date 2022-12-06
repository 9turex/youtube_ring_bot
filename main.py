from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import telegram_api_token
from services.youtube_requests import YouTubeRequest
from services.telegram import register_handlers_tg


def on_startup():
    print('bot started')


bot = Bot(telegram_api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers_tg(dp)

executor.start_polling(dp, on_startup=on_startup())
