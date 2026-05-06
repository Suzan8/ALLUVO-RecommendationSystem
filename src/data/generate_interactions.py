import pandas as pd
import numpy as np
import random
import os
import json
from datetime import timedelta

np.random.seed(42)

DATA_PATH = "data/raw/interactions.csv"


# =========================
# Core generator (FIXED)
# =========================
def generate_interactions(users_df, reels_df):

    interactions = []

    for _, user in users_df.iterrows():

        interests = user["interests"]
        followed_brands = user["followed_brands"]

        if isinstance(interests, str):
            interests = json.loads(interests)

        if isinstance(followed_brands, str):
            followed_brands = json.loads(followed_brands)

        # 🔥 FIX: منع crash لو الداتا قليلة
        sample_size = min(len(reels_df), random.randint(50, 150))
        if sample_size == 0:
            continue

        reel_sample = reels_df.sample(n=sample_size)

        for _, reel in reel_sample.iterrows():

            p = 0.1

            if reel["category"] in interests:
                p = 0.6
            elif reel["brand_id"] in followed_brands:
                p = 0.3

            if np.random.rand() >= p:
                continue

            like = int(np.random.rand() < 0.3)
            comment = int(np.random.rand() < 0.1)
            purchase = int(np.random.rand() < 0.03)

            watch_ratio = round(random.uniform(0.1, 1.0), 2)

            if reel["category"] in interests or reel["brand_id"] in followed_brands:
                watch_ratio = round(random.uniform(0.5, 1.0), 2)

            timestamp = pd.to_datetime(
                reel["created_at"],
                format="%Y-%m-%d %H:%M:%S",
                errors="coerce"
            )

            if pd.isna(timestamp):
                continue

            timestamp = timestamp + timedelta(days=random.randint(0, 10))
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            interaction = {
                "user_id": user["user_id"],
                "reel_id": reel["reel_id"],
                "view": 1,
                "watch_ratio": watch_ratio,
                "like": like,
                "comment": comment,
                "purchase": purchase,
                "timestamp": timestamp
            }

            interactions.append(interaction)

    return pd.DataFrame(interactions)


# =========================
# Smart loader (FIXED)
# =========================
def get_interactions():

    if os.path.exists(DATA_PATH):
        print("📂 Loading existing interactions dataset...")

        df = pd.read_csv(DATA_PATH)

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        )

        df = df.dropna(subset=["timestamp"])

        return df

    print("⚙️ Generating interactions dataset...")

    from src.data.generate_users import get_users
    from src.data.generate_reels import get_reels

    users_df = get_users()
    reels_df = get_reels()

    df = generate_interactions(users_df, reels_df)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print("Total interactions:", len(df))

    return df