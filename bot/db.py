import os
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "monetag_bot")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]

async def init_db():
    # No-op for MongoDB, but can be used for index creation
    await users.create_index("user_id", unique=True)

async def add_user(user_id, username):
    await users.update_one({"user_id": user_id}, {"$setOnInsert": {"user_id": user_id, "username": username, "points": 0.0}}, upsert=True)

async def add_points(user_id, amount):
    await users.update_one({"user_id": user_id}, {"$inc": {"points": amount}})

async def get_points(user_id):
    user = await users.find_one({"user_id": user_id})
    return user["points"] if user and "points" in user else 0.0

async def get_user_count():
    return await users.count_documents({})

async def get_all_users():
    return users.find({})
