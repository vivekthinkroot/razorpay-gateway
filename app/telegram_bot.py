import httpx
from .config import settings

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

async def get_first_chat_id():
    url = f"{TELEGRAM_API_BASE}/getUpdates"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        updates = response.json()
        # Extract the latest valid chat_id
        for result in reversed(updates.get("result", [])):
            message = result.get("message")
            if message and "chat" in message:
                return message["chat"]["id"]
    raise Exception("No chat_id found. Please send a message to the bot first.")

async def send_payment_link_to_telegram(link: str, name: str):
    chat_id = await get_first_chat_id()
    message = f"Hi {name}, please complete your payment:\n{link}"
    url = f"{TELEGRAM_API_BASE}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)
        response.raise_for_status()
