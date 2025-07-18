from pydantic import BaseModel, EmailStr

class CreatePaymentLinkRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    amount: int  # in INR

class PaymentLinkResponse(BaseModel):
    id: str
    status: str
    short_url: str
