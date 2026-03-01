import stripe
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
YOUR_DOMAIN = "http://localhost:8501"

def create_checkout_session(amount=500, currency="usd", style="Classic Cartoon"):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "unit_amount": amount,
                    "product_data": {
                        "name": f"Toonify - {style} Style",
                        "description": "Download your cartoonized image",
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=YOUR_DOMAIN + "?payment=success",
            cancel_url=YOUR_DOMAIN + "?payment=cancel",
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Stripe error: {e}")
        return None