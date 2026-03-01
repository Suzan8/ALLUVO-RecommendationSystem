# src/data/generate_reels.py

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

def generate_reels(num_reels=3000, brands_df=None):
    if brands_df is None:
        raise ValueError("brands_df must be provided")

    reels = []

    for i in range(1, num_reels + 1):
        brand_id = random.randint(1, len(brands_df))  # اختيار براند عشوائي
        category = brands_df.loc[brands_df['brand_id'] == brand_id, 'category'].values[0]

        reel = {
            "reel_id": i,
            "brand_id": brand_id,
            "category": category,
            "price": round(random.uniform(10, 500), 2),
            "created_at": datetime.now() - timedelta(days=random.randint(0, 90)),
            "video_duration": random.randint(10, 60)  # بالثواني
        }
        reels.append(reel)

    return pd.DataFrame(reels)


if __name__ == "__main__":
    # لازم نقرأ Brands CSV الأول
    brands_df = pd.read_csv("data/raw/brands.csv")
    df = generate_reels(brands_df=brands_df)
    df.to_csv("data/raw/reels.csv", index=False)
    print("Reels dataset generated successfully.")