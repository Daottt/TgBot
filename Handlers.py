import Config
from main import bot, dp
import models
from Config import AdminId

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

categorys = ["Про штирлица", "Другие", "Про мужика"]
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Про штирлица"), KeyboardButton(text="Другие"), KeyboardButton(text="Про мужика")]
    ],
    resize_keyboard=True
)
mod = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить"), KeyboardButton(text="Отклонить"), KeyboardButton(text="Выход")]
    ],
    resize_keyboard=True
)

class Form(StatesGroup):
    choiceCategory = State()
    addJoke = State()
    moderating = State()


@dp.message_handler(Command("start"))
async def Start(message: Message):
    await message.answer("Выберите тип анекдота \nчто бы добавить свой напишите /add", reply_markup=menu)


@dp.message_handler(Text(equals=["Другие", "Про штирлица", "Про мужика"]))
async def anek(message: Message):
    text = models.GetRandomJoke(message.text)
    await message.answer(text)

@dp.message_handler(Command("add"))
async def AddJoke(message: Message):
    await message.answer("Выберете категорию добавляемого анекдота", reply_markup=menu)
    await Form.choiceCategory.set()

@dp.message_handler(Command("moderate"))
async def moderating(message: Message, state: FSMContext):
    if(message.from_user.id != int(AdminId)):
        return

    await Form.moderating.set()
    curJoke = models.GetNotModeratedJoke()
    if curJoke == None:
        await message.answer("Модерировать больше нечего")
        await state.finish()
        await Start(message)
        return
    await state.update_data(currentJoke = curJoke)
    await message.answer(f"Категория : {curJoke[0]} \nТекст : {curJoke[1]}", reply_markup=mod)

@dp.message_handler(state=Form.moderating)
async def jokeModerating(message: Message, state: FSMContext):

    data = await state.get_data()
    curJoke = data.get("currentJoke")

    if (message.text == "Добавить"):
        models.ModerateJoke(curJoke[1])
        await message.answer("Анекдот добавлен")
        await moderating(message, state)
    elif(message.text == "Отклонить"):
        models.DeleteJoke(curJoke[1])
        await message.answer("Анекдот отклонен")
        await moderating(message, state)
    else:
        await message.answer("Выход из режима модератора")
        await state.finish()
        await Start(message)


@dp.message_handler(state=Form.choiceCategory)
async def ChoiceCategory(message: Message, state: FSMContext):
    text = message.text
    if not categorys.__contains__(text):
        await message.answer("Введена неправильная категория. Выберете одну из указанных", reply_markup=menu)
        return
    await message.answer("Введите текст анекдота")
    await state.update_data(category=text)
    await Form.addJoke.set()

@dp.message_handler(state=Form.addJoke)
async def SendJoke(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")

    if(message.from_user.id == int(AdminId)):
        models.AddJoke(category, message.text)
        models.ModerateJoke(message.text)
        await message.answer("Ваш анекдот добавлен", reply_markup=menu)
    else:
        models.AddJoke(category, message.text)
        await message.answer("Ваш анекдот отправлен на проверку", reply_markup=menu)


    await state.finish()
    #await bot.send_message(chat_id=AdminId, text=f"Добавлен анекдот в категорию: {category} текст: {message.text}")



