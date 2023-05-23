from peewee import *
from .config import config

db = PostgresqlDatabase(
    config("db", "name"),
    user=config("db", "user"),
    password=config("db", "password"),
    host=config("db", "host"),
    port=config("db", "port"),
)
