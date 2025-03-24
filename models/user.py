from .base import BaseSchema
from typing import Optional , List

class UserSchema(BaseSchema):
    username:str
    telegram_id:str
    first_name:str
    last_name:str
    merchant_name:Optional[str]=None
    isAdmin:bool = False
    wallet_addresses:Optional[List[str]] = None
    total_transactions:int=0
    logo_url:Optional[str] = None

class UpdateUser(BaseSchema):
    username:Optional[str]
    first_name:Optional[str]
    last_name:Optional[str]
    merchant_name:Optional[str]
    logo_url:Optional[str]