from database.collections import payments_collection
from models.payment import PaymentSchema


async def create_payment(payment:PaymentSchema):
    payment_dict = payment.dict(by_alias=True)
    result = await payments_collection.insert_one(payment_dict)
    return {**payment_dict, "_id": str(result.inserted_id)}

async def get_payment_by_user_id(user_id:str):
    try:
        payment = await payments_collection.find_one({"user_id":user_id})
        if payment:
          payment["_id"] = str(payment["_id"])
          return payment
    except Exception as e:
        print(e)


async def get_payment(reference:str):
    try:
        payment = await payments_collection.find_one({"reference":payment_id})
        if payment:
          payment["_id"] = str(payment["_id"])
          return payment
    except Exception as e:
        print(e)
        return None

async def get_payments(page:int=1, limit:int=10):
    skip = (page-1)*limit
    payments = await payments_collection.find().skip(skip).limit(limit).to_list(length=limit)
    for payment in payments:
        payment["_id"] = str(payment["_id"])
    return payments

async def get_payments_count():
    return await payments_collection.count_documents({})



   
