# src/data/generate_users.py

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def generate_age():
    r = random.random()
    if r < 0.35:
        return random.randint(18, 24)
    elif r < 0.75:
        return random.randint(25, 34)
    elif r < 0.95:
        return random.randint(35, 45)
    else:
        return random.randint(46, 60)


def generate_interests(categories):
    return random.sample(categories, random.randint(2, 4))


def generate_followed_brands(num_brands=30):
    return random.sample(range(1, num_brands + 1), random.randint(1, 5))


def generate_users(num_users=2000):
    categories = [
        "Fashion",
        "Beauty",
        "Fitness",
        "Technology",
        "Home",
        "Sports",
        "Gaming"
    ]

    users = []

    for i in range(1, num_users + 1):
        user = {
            "user_id": i,
            "age": generate_age(),
            "gender": random.choice(["Male", "Female"]),
            "interests": generate_interests(categories),
            "followed_brands": generate_followed_brands(),
            "created_at": datetime.now() - timedelta(days=random.randint(0, 365))
        }
        users.append(user)

    return pd.DataFrame(users)


if __name__ == "__main__":
    df = generate_users()
    df.to_csv("data/raw/users.csv", index=False)
    print("Users dataset generated successfully.")