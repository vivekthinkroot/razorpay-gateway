import httpx
from .config import settings

auth = (settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)

async def create_payment_link(data: dict):
    url = f"{settings.RAZORPAY_BASE_URL}/payment_links"

    # Log start of request
    print("🔄 Sending payment link request to Razorpay...")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            auth=auth
        ) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            print("✅ Razorpay responded successfully.")
            return response.json()

    except httpx.HTTPStatusError as exc:
        print(f"❌ HTTP error from Razorpay: {exc.response.status_code} - {exc.response.text}")
        raise

    except httpx.RequestError as exc:
        print(f"❌ Network error while calling Razorpay: {exc}")
        raise

async def get_payment_status(link_id: str):
    url = f"{settings.RAZORPAY_BASE_URL}/payment_links/{link_id}"

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"❌ Error fetching payment status: {e}")
        raise

async def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getUpdates"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
        chat_id = data["result"][-1]["message"]["chat"]["id"]  # last chat ID
        send_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        await client.post(send_url, json=payload)
