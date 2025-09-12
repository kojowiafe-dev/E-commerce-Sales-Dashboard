import random
from datetime import datetime, timedelta

def generate_otp():
    return str(random.randint(100000, 999999))


def get_expiry(minutes=10):
    return datetime.utcnow() + timedelta(minutes=minutes)