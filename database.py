from peewee import CharField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase('yacht.db')


class Records(Model):
    name = CharField()
    yacht = CharField()
    points = IntegerField()
    track = IntegerField()

    class Meta:
        database = db
