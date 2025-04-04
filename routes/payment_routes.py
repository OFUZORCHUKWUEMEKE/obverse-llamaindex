from fastapi import APIRouter, HTTPException
from repositories.payment_repository import create_payment,get_payment,get_payments_count,get_payment_by_user_id
from models.payment import PaymentSchema

router = APIRouter()

@router.post("/payments")
async def create_payment_endpoint(payment:PaymentSchema):
    return await create_payment(payment)

@router.get("/payments/count")
async def get_payments_count_endpoint():
    return await get_payments_count()

@router.get("/payment/{user_id}")
async def get_payment_by_user_id_endpoint(user_id:str):
    payment = await get_payment_by_user_id(user_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/payments/{reference}")
async def get_payment_endpoint(reference:str):
    payment = await get_payment(reference)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/payments")
async def get_payments_endpoint(page:int=1, limit:int=10):
    payments = await get_payments(page=page, limit=limit)
    if not payments:
        raise HTTPException(status_code=404, detail="Payments not found")
    return payments