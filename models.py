from random import choice
from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Joke(BaseModel):
    category_name = TextField(null=False)
    text = TextField(null=False)
    moderated = BooleanField(default=False)


db.connect()

db.create_tables([Joke])

def AddJoke(category, joke_text):
    joke = Joke.get_or_create(category_name=category, text=joke_text)

def GetRandomJoke(category):
    try:
        with db:
            jokes = Joke.select().where(Joke.category_name == category,
                                        Joke.moderated == True)  # ВЫБОР ПО КАТЕГОРИИ НЕ РАБОТЕТ
            joke = choice(jokes)
            return joke.text
    except:
        return "Анекдотов нету"

def GetNotModeratedJoke():
    try:
        with db:
            jokes = Joke.select().where(Joke.moderated == False)
            joke = choice(jokes)
            return joke.category_name, joke.text
    except:
        return None

def ModerateJoke(joke_text):
    with db:
        joke = Joke.get(Joke.text == joke_text)
        joke.moderated = True
        joke.save()

def DeleteJoke(joke_text):
    with db:
        joke = Joke.get(Joke.text == joke_text)
        joke.delete_instance()

