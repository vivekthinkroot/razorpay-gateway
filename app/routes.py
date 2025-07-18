from fastapi import APIRouter, HTTPException
from .models import CreatePaymentLinkRequest, PaymentLinkResponse
from .razorpay_client import create_payment_link
from .telegram_bot import send_payment_link_to_telegram
from .razorpay_client import get_payment_status, send_telegram_message

router = APIRouter()

@router.post("/send-link", response_model=PaymentLinkResponse)
async def send_link(payload: CreatePaymentLinkRequest):
    try:
        razorpay_payload = {
            "amount": payload.amount * 100,
            "currency": "INR",
            "customer": {
                "name": payload.name,
                "email": payload.email,
                "contact": payload.phone
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True
        }
        response = await create_payment_link(razorpay_payload)

        await send_payment_link_to_telegram(response["short_url"], payload.name)

        return {
            "id": response["id"],
            "status": response["status"],
            "short_url": response["short_url"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from .razorpay_client import get_payment_status, send_telegram_message

@router.get("/payment-status/{link_id}")
async def payment_status(link_id: str):
    status_data = await get_payment_status(link_id)
    
    status = status_data["status"]
    paid = status == "paid"
    masked_id = '*' * (len(link_id) - 5) + link_id[-5:]

    
    msg = (
        f"✅ Payment received for link ID {link_id}.\nAmount: ₹{status_data['amount'] / 100}"
        if paid else
        f"❌ Payment not completed yet for link ID {masked_id}."
    )
    
    await send_telegram_message(msg)

    return {
        "id": status_data["id"],
        "status": status_data["status"],
        "paid": paid,
        "short_url": status_data["short_url"]
    }
