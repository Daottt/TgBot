import Config
from main import bot, dp
import models
from Config import AdminId

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Про штирлица"), KeyboardButton(text="Другие"), KeyboardButton(text="Про мужика")]
    ],
    resize_keyboard=True
)

class Form(StatesGroup):
    choiceCategory = State()
    addJoke = State()


@dp.message_handler(Command("start"))
async def Start(message: Message):
    await message.answer("Выберете тип анекдота что бы добавить свой напишите /add", reply_markup=menu)


@dp.message_handler(Text(equals=["Другие", "Про штирлица", "Про мужика"]))
async def anek(message: Message):
    text = models.GetRandomJoke(message.text)
    await message.answer(text)

@dp.message_handler(Command("add"))
async def AddJoke(message: Message):
    await message.answer("Выберете категорию затем введите анекдот", reply_markup=menu)
    await Form.choiceCategory.set()

@dp.message_handler(state=Form.choiceCategory)
async def ChoiceCategory(message: Message, state: FSMContext):
    text = message.text

    await state.update_data(category=text)
    await Form.addJoke.set()

@dp.message_handler(state=Form.addJoke)
async def SendJoke(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")

    models.AddJoke(category, message.text)
    await message.answer("Ваш анекдот добавлен", reply_markup=menu)

    await state.finish()



