from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Razorpay + Telegram Microservice")

app.include_router(router)
