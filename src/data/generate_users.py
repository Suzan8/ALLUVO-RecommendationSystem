import pandas as pd
import numpy as np
import random
import os
import json
from datetime import datetime, timedelta

np.random.seed(42)

DATA_PATH = "data/raw/users.csv"
num_users = 2000


# =========================
# Age distribution
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
# Interests
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
# Safe datetime
# =========================
def generate_created_at():
    dt = datetime.now() - timedelta(days=random.randint(0, 365))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# =========================
# Core generator
# =========================
def generate_users():
    users = []

    for i in range(1, num_users + 1):
        users.append({
            "user_id": i,
            "age": generate_age(),
            "gender": random.choice(["Male", "Female"]),
            "interests": json.dumps(generate_interests()),  # JSON string
            "followed_brands": json.dumps(generate_followed_brands()),  # JSON string
            "created_at": generate_created_at()
        })

    return pd.DataFrame(users)


# =========================
# SAFE JSON parser (🔥 مهم جدا)
# =========================
def safe_json_load(x):
    try:
        if isinstance(x, list):
            return x
        if pd.isna(x):
            return []
        return json.loads(x)
    except:
        return []


# =========================
# Loader (FINAL FIX)
# =========================
def get_users():

    if os.path.exists(DATA_PATH):
        print("📂 Loading existing users dataset...")

        users_df = pd.read_csv(DATA_PATH)

        # 🔥 FIX datetime parsing (no warning)
        users_df["created_at"] = pd.to_datetime(
            users_df["created_at"],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        )

        users_df = users_df.dropna(subset=["created_at"])

        # 🔥 FIX JSON corruption
        users_df["interests"] = users_df["interests"].apply(safe_json_load)
        users_df["followed_brands"] = users_df["followed_brands"].apply(safe_json_load)

        return users_df

    print("⚙️ Generating users dataset...")

    users_df = generate_users()

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    users_df.to_csv(DATA_PATH, index=False)

    return users_df