import json
from random import choice
from main import bot, dp

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Command,Text

with open("anekdotbl.json", "r", encoding="utf-8") as JokeJson:
    JokeData = json.load(JokeJson)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Про штирлица"), KeyboardButton(text="Другие"), KeyboardButton(text="Про мужика")]
    ],
    resize_keyboard=True
)


@dp.message_handler(Command("start"))
async def Start(message: Message):
    await message.answer("Выберете тип анекдота", reply_markup=menu)


@dp.message_handler(Text(equals=["Другие", "Про штирлица", "Про мужика"]))
async def anek(message: Message):
    text = choice(JokeData[message.text])
    await message.answer(text)

