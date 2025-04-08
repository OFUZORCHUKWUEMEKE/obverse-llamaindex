# from .base import BaseSchema
from enum import Enum
from datetime import datetime
from typing import Optional , Dict , Any,List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


PyObjectId = Annotated[str, BeforeValidator(str)]


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"

class Chain(str, Enum):
    SOLANA = "solana"

class Currency(str,Enum):
    USDT="usdt"

class PaymentSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    amount: float
    currency:str=Currency.USDT
    user_id: str
    status: PaymentStatus = PaymentStatus.PENDING
    chain: Chain = Chain.SOLANA
    reference: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    details: List[str] = []
    title: Optional[str]
    description: Optional[str] = None
    logo_url: Optional[str] = None
    model_config= ConfigDict(
        populate_by_name=True,
        aarbitrary_types_allowed=True,
    )

class PaymentCollection(BaseModel):
    payments:List[PaymentSchema]