# src/data/generate_interactions.py

import pandas as pd
import numpy as np
import random
from datetime import timedelta

np.random.seed(42)

def generate_interactions(users_df, reels_df):
    interactions = []

    for idx, user in users_df.iterrows():
        # كل مستخدم يتفاعل مع 50–150 Reel بشكل محتمل
        num_reels_to_interact = random.randint(50, 150)
        reel_sample = reels_df.sample(n=num_reels_to_interact)

        for _, reel in reel_sample.iterrows():
            # حساب احتمالية التفاعل
            p = 0.1
            if reel['category'] in user['interests']:
                p = 0.6
            elif reel['brand_id'] in user['followed_brands']:
                p = 0.3

            interacted = np.random.rand() < p
            if not interacted:
                continue  # تجاهل لو المستخدم لم يتفاعل

            # أنواع التفاعل
            like = int(np.random.rand() < 0.3)
            comment = int(np.random.rand() < 0.1)
            purchase = int(np.random.rand() < 0.03)
            watch_ratio = round(random.uniform(0.1, 1.0), 2)
            if reel['category'] in user['interests'] or reel['brand_id'] in user['followed_brands']:
                watch_ratio = round(random.uniform(0.5, 1.0), 2)

            interaction = {
                "user_id": user['user_id'],
                "reel_id": reel['reel_id'],
                "view": 1,
                "watch_ratio": watch_ratio,
                "like": like,
                "comment": comment,
                "purchase": purchase,
                "timestamp": reel['created_at'] + timedelta(days=random.randint(0, 10))
            }
            interactions.append(interaction)

    return pd.DataFrame(interactions)


if __name__ == "__main__":
    users_df = pd.read_csv("data/raw/users.csv")
    reels_df = pd.read_csv("data/raw/reels.csv")

    import ast
    users_df['interests'] = users_df['interests'].apply(ast.literal_eval)
    users_df['followed_brands'] = users_df['followed_brands'].apply(ast.literal_eval)

    # تحويل created_at في reels لـ datetime
    reels_df['created_at'] = pd.to_datetime(reels_df['created_at'])

    interactions_df = generate_interactions(users_df, reels_df)
    interactions_df.to_csv("data/raw/interactions.csv", index=False)
    print("Interactions dataset generated successfully.")
    print("Total interactions:", len(interactions_df))