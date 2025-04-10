from fastapi import APIRouter, HTTPException
from repositories.payment_repository import create_payments,get_payment,get_payment_by_user_id,get_payments
from models.payment import PaymentSchema

router = APIRouter()

@router.post("/payments")
async def create_payment_endpoint(payment:PaymentSchema):
    return await create_payments(payment)


# @router.get("/payment/{user_id}")
# async def get_payment_by_user_id_endpoint(user_id:str):
#     payment = await get_payment_by_user_id(user_id)
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")
#     return payment

@router.get("/payments/{reference}")
async def get_payment_endpoint(reference:str):
    payment = await get_payment(reference)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/payments")
async def get_payments_endpoint(page:int=1, limit:int=10):
    payments = await get_payments()
    if not payments:
        raise HTTPException(status_code=404, detail="Payments not found")
    return payments