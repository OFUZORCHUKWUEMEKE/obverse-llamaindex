from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.payment_routes import router as payment_router
from database.collections import create_indexes

app = FastAPI(title="Crypto Payment API")

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(payment_router, prefix="/api/v1", tags=["payments"])

app.on_event("startup")
async def startup_event():
    await create_indexes()

app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)