from datetime import datetime
from typings import Optional
from pydantic import BaseModel
from enum import Enum
from core.config import config

class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"

class Chain(Enum):
    SOLANA='solana'

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
   
    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

class PaymentSchema(BaseModel):
    amount:float
    currency:str
    type:Optional[str]=None
    status:PaymentStatus=PaymentStatus.PENDING
    user_id:str
    payment_link:str
    chain:Chain=Chain.SOLANA
    reference:str
    transaction_hash:Optional[str]
    expires_at:Optional[datetime]
    metadata:Optional[Dict[str, any]] = None
    logo_url:Optional[str]
    created_at:datetime=datetime.now()
    updated_at:datetime=datetime.now()

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

# MongoDB connection
client = MongoClient(config.MONGO_URL)
db = client["obverse_dev"]