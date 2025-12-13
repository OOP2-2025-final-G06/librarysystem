from peewee import Model, CharField, IntegerField
from .db import db

class Product(Model):
    title = CharField()
    genre = CharField()
    maxNumber = IntegerField()
    currentNumber = IntegerField()

    class Meta:
        database = db
