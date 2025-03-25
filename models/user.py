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
    username:Optional[str]=None
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    merchant_name:Optional[str]=None
    logo_url:Optional[str]=None
    wallet_addresses:Optional[str]=None