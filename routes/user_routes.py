from fastapi import APIRouter,HTTPException
from repositories.user_repository import create_user , get_user
from models.user import UserSchema
from typing import Optional

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(user:UserSchema):
    return await create_user(user)

@router.get("/users/{telegram_id}")
async def get_user_endpoint(telegram_id:str):
    user = await get_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user