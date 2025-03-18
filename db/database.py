from pymongo import MongoClient
from core.config import config
from fastapi import Depends

client = MongoClient(config.MONGO_URI)
db = client.get_default_database()

def get_db():
    yield db