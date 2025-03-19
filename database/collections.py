from .connection import database
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

users_collection = database["users"]
payments_collection = database["payments"]

async def create_indexes():
    """Create unique indexes in MongoDB."""
    await users_collection.create_index("telegram_id",unique=True)
    await payments_collection.create_index("reference",unique=True)
    print("✅ Indexes created successfully.")

