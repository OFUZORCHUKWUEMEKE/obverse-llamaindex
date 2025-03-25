from database.collections import users_collection
from models.user import UserSchema, UpdateUser
from bson import ObjectId

async def create_user(user:UserSchema):
    user_dict = user.dict(by_alias=True)
    result = await users_collection.insert_one(user_dict)
    return {**user_dict, "_id":str(result.inserted_id)}

async def get_user(telegram_id:str):
    user = await users_collection.find_one({"telegram_id":telegram_id})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_user_by_id(id:str):
    user = await users_collection.find_one({"_id":ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_users(page:int=1, limit:int=10):
    skip = (page-1)*limit
    users = await users_collection.find().skip(skip).limit(limit).to_list(length=limit)
    return users

async def update_user(telegram_id:str, user:UpdateUser):
    user_dict = user.dict(exclude_none=True)
    await users_collection.update_one({"telegram_id":telegram_id}, {"$set":user_dict})
    return {"message":"User updated successfully"}

async def delete_user(telegram_id:str):
    await users_collection.delete_one({"telegram_id":telegram_id})
    return {"message":"User deleted successfully"}



