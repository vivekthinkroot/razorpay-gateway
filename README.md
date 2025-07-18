# Razorpay + Telegram Microservice

A FastAPI-based microservice to generate Razorpay payment links and send them to users via Telegram.  
It also allows checking payment status and notifies the user on Telegram.

## Features

- Create Razorpay payment links via API
- Send dynamic payment links to users on Telegram
- Check payment status and notify via Telegram

## Requirements

- Python 3.8+
- A Razorpay account (API key & secret)
- A Telegram bot token (and a user who has messaged the bot)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/vivekthinkroot/razorpay-gateway.git
   cd razorpay-gateway
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   pip install pydantic-settings
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root with the following content:
   ```env
   RAZORPAY_API_KEY=your_razorpay_api_key
   RAZORPAY_API_SECRET=your_razorpay_api_secret
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   RAZORPAY_BASE_URL=https://api.razorpay.com/v1
   ```

## Usage

1. **Start the server:**
   ```sh
   uvicorn app.main:app --reload --port 8000
   ```

2. **API Endpoints:**

   - **POST `http://localhost:8000/send-link`**  
     Create a payment link and send it to a user on Telegram.
     ```json
     {
       "amount": 100,
       "name": "John Doe",
       "email": "john@example.com",
       "phone": "9876543210"
     }
     ```
     **Response:**
     ```json
     {
       "id": "plink_xxxxx",
       "status": "created",
       "short_url": "https://rzp.io/i/xxxx"
     }
     ```

   - **GET `http://localhost:8000/payment-status/{link_id}`**  
     Check the payment status for a given payment link.  
     Notifies the user on Telegram about the payment status.

     **Response:**
     ```json
     {
       "id": "plink_xxxxx",
       "status": "paid",
       "paid": true,
       "short_url": "https://rzp.io/i/xxxx"
     }
     ```

## Notes

- The Telegram bot must have received at least one message from the user to send messages.
- The `.env` file is required for configuration.


