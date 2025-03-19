from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.payment_routes import router as payment_router

app = FastAPI(title="Crypto Payment API")

app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(payment_router, prefix="/api/v1", tags=["payments"])


app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)