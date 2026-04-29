import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

np.random.seed(42)

DATA_PATH = "data/raw/users.csv"

num_users = 2000

# =========================
# Age distribution (18-60)
# =========================
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


# =========================
# Interests (7 categories)
# =========================
categories = ["Fashion", "Beauty", "Fitness", "Technology", "Home", "Sports", "Gaming"]

def generate_interests():
    return random.sample(categories, random.randint(2, 4))


# =========================
# Followed brands
# =========================
def generate_followed_brands():
    return random.sample(range(1, 31), random.randint(1, 5))


# =========================
# Core generator (NO CHANGE)
# =========================
def generate_users():
    users = []

    for i in range(1, num_users + 1):
        user = {
            "user_id": i,
            "age": generate_age(),
            "gender": random.choice(["Male", "Female"]),
            "interests": generate_interests(),
            "followed_brands": generate_followed_brands(),
            "created_at": datetime.now() - timedelta(days=random.randint(0, 365))
        }
        users.append(user)

    return pd.DataFrame(users)


# =========================
# Smart loader (NEW - important)
# =========================
def get_users():
    """
    - If file exists → load it
    - Else → generate + save it
    """

    if os.path.exists(DATA_PATH):
        print("📂 Loading existing users dataset...")
        return pd.read_csv(DATA_PATH)

    print("⚙️ Generating users dataset...")
    users_df = generate_users()

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    users_df.to_csv(DATA_PATH, index=False)

    return users_df


