from .base import BaseSchema
from enum import Enum
from datetime import datetime
from typing import Optional , Dict , Any


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"

class Chain(str, Enum):
    SOLANA = "solana"

class PaymentSchema(BaseSchema):
    amount: float
    currency: str
    user_id: str
    status: PaymentStatus = PaymentStatus.PENDING
    chain: Chain = Chain.SOLANA
    reference: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    details: Dict[str, Any] = {}