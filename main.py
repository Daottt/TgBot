import asyncio

from aiogram import Bot, Dispatcher, executor
from Config import BotToken

bot = Bot(BotToken)
dp = Dispatcher(bot)



if __name__ == '__main__':
    from Handlers import dp
    executor.start_polling(dp)