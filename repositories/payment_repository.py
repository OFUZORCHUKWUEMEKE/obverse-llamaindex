from database.collections import payments_collection
from models.payment import PaymentSchema,PaymentCollection
from bson import ObjectId

async def create_payments(payment:PaymentSchema):
    """
    Create a new Payment handler
    """
    new_payments = await payments_collection.insert_one(
        payment.model_dump(by_alias=True,exclude=["id"])
    )
    create_payments= await payments_collection.find_one({"_id":new_payments.inserted_id})
    return create_payments

async def get_payment_by_user_id(user_id:str):
    if(
        payment := payments_collection.find({"user_id":user_id})
    ) is not None:
       return payment


async def get_payment(reference:str):
    """
    Get Payment by Reference
    """
    if(
        payment := payments_collection.find_one({"reference":reference})
    )is not None:
        return payment

async def get_payments(page:int=1, limit:int=10):
    """
    Get all Payments in the Platform
    """
    return PaymentCollection(payments = await payments_collection.find({}).to_list(1000))



   
