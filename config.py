import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    DATABASE = "ecommerce.db"
    STRIPE_SECRET_KEY = "your_stripe_secret_key"
