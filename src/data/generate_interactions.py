import pandas as pd
import numpy as np
import random
import os
from datetime import timedelta

np.random.seed(42)

DATA_PATH = "data/raw/interactions.csv"


# =========================
# Core generator (NO CHANGE)
# =========================
def generate_interactions(users_df, reels_df):

    interactions = []

    for _, user in users_df.iterrows():

        num_reels_to_interact = random.randint(50, 150)
        reel_sample = reels_df.sample(n=num_reels_to_interact)

        for _, reel in reel_sample.iterrows():

            p = 0.1

            if reel["category"] in user["interests"]:
                p = 0.6
            elif reel["brand_id"] in user["followed_brands"]:
                p = 0.3

            interacted = np.random.rand() < p
            if not interacted:
                continue

            like = int(np.random.rand() < 0.3)
            comment = int(np.random.rand() < 0.1)
            purchase = int(np.random.rand() < 0.03)

            watch_ratio = round(random.uniform(0.1, 1.0), 2)

            if reel["category"] in user["interests"] or reel["brand_id"] in user["followed_brands"]:
                watch_ratio = round(random.uniform(0.5, 1.0), 2)

            interaction = {
                "user_id": user["user_id"],
                "reel_id": reel["reel_id"],
                "view": 1,
                "watch_ratio": watch_ratio,
                "like": like,
                "comment": comment,
                "purchase": purchase,
                "timestamp": reel["created_at"] + timedelta(days=random.randint(0, 10))
            }

            interactions.append(interaction)

    return pd.DataFrame(interactions)


# =========================
# Smart loader
# =========================
def get_interactions():

    if os.path.exists(DATA_PATH):
        print("📂 Loading existing interactions dataset...")
        return pd.read_csv(DATA_PATH)

    print("⚙️ Generating interactions dataset...")

    # dependencies
    from src.data.generate_users import get_users
    from src.data.generate_reels import get_reels

    users_df = get_users()
    reels_df = get_reels()

    df = generate_interactions(users_df, reels_df)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print("Total interactions:", len(df))

    return df


