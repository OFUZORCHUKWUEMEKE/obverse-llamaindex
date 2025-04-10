from database.collections import users_collection
from models.user import UserSchema, UpdateUser , UserCollection
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response

async def getUsers():
    return UserCollection(users = await users_collection.find({}).to_list(100))

async def create_user(user:UserSchema):
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True,exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id":new_user.inserted_id}
    )
    return created_user

async def get_user(telegram_id:str):
    if(
        user:= await users_collection.find_one({"telegram_id":telegram_id})
    )is not None:
        return user
    raise HTTPException(status_code=404,detail=f"student {id} not found")



async def get_user_by_id(id:str):
   if(
      user:= await users_collection.find_one({"_id":ObjectId(id)})
   ) is not None:
      return user


async def update_user(telegram_id:str, user:UpdateUser):
    user_dict = user.dict(exclude_none=True)
    await users_collection.update_one({"telegram_id":telegram_id}, {"$set":user_dict})
    return {"message":"User updated successfully"}



