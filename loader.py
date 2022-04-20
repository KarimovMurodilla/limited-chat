from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from connection import Sqlither

bot = Bot(token=BOT_TOKEN, parse_mode = 'html')
dp = Dispatcher(bot)

db = Sqlither('database.db')
