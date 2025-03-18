from datetime import datetime
from typings import Optional
from pydantic import BaseModel
from enum import Enum

class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"

class UserSchema(BaseModel):
    username:str
    telegram_id:str
    first_name:str
    last_name:str
    merchant_name:Optional[str]=None
    isAdmin:bool = False
    wallet_addresses:Optional[List[str]] = None
    total_transactions:int=0
    logo_url:Optional[str] = None


class PaymentSchema(BaseModel):
    amount:float
    currency:str
    type:Optional[str]=None
    status:PaymentStatus=PaymentStatus.PENDING
    user_id:str