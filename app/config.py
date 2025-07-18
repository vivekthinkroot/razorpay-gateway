from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RAZORPAY_API_KEY: str
    RAZORPAY_API_SECRET: str
    TELEGRAM_BOT_TOKEN: str
    RAZORPAY_BASE_URL: str = "https://api.razorpay.com/v1"

    class Config:
        env_file = ".env"

settings = Settings()
