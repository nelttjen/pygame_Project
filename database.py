from peewee import *

db = SqliteDatabase('yacht.db')

class Records(Model):
    name = CharField()
    yacht = CharField()
    points = IntegerField()
    track = IntegerField()

    class Meta:
        database = db
