import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config import BotToken

bot = Bot(BotToken)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def shutdown(dp):
    await storage.close()

if __name__ == '__main__':
    from Handlers import dp
    executor.start_polling(dp, on_shutdown=shutdown)
