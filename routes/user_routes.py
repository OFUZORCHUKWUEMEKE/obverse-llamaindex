from fastapi import APIRouter,HTTPException
from repositories.user_repository import create_user , get_user,getUsers
from models.user import UserSchema,UserCollection
from typing import Optional

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(user:UserSchema):
    return await create_user(user)

@router.get("/users/{telegram_id}",response_model=UserSchema)
async def get_user_endpoint(telegram_id:str):
    user = await get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users",response_model=UserCollection)
async def getAllUsers():
    user = await getUsers()
    if not user:
        raise HTTPException(status_code=400,detail="User not found")
    return user