from peewee import SqliteDatabase

db = SqliteDatabase('my_database.db', check_same_thread=False)