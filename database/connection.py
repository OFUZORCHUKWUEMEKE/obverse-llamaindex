import os
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = os.getenv("MONGO_URL")
DB_NAME="obverse_dev"
client = AsyncIOMotorClient(config.MONGO_URI)

client = client.get_default_database()
database = client[DB_NAME]