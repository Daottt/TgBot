from random import choice
from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Joke(BaseModel):
    category_name = TextField(null=False)
    text = TextField(null=False)


db.connect()

db.create_tables([Joke])

def AddJoke(category, joke_text):
    joke = Joke.get_or_create(category_name=category, text=joke_text)

def GetRandomJoke(category):
    with db:
        jokes = Joke.select().where(Joke.category_name == category)
        joke = choice(jokes)
        return joke.text
