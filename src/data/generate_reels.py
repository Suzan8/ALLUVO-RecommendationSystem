import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

np.random.seed(42)

DATA_PATH = "data/raw/reels.csv"
num_reels = 3000


# =========================
# Safe datetime
# =========================
def generate_created_at():
    dt = datetime.now() - timedelta(days=random.randint(0, 90))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# =========================
# Core generator
# =========================
def generate_reels(brands_df):
    reels = []

    for i in range(1, num_reels + 1):
        brand_id = random.randint(1, 30)

        category = brands_df.loc[
            brands_df["brand_id"] == brand_id, "category"
        ].values[0]

        reel = {
            "reel_id": i,
            "brand_id": brand_id,
            "category": category,
            "price": round(random.uniform(10, 500), 2),
            "created_at": generate_created_at(),
            "video_duration": random.randint(10, 60)
        }

        reels.append(reel)

    return pd.DataFrame(reels)


# =========================
# Smart loader (FIXED)
# =========================
def get_reels():

    if os.path.exists(DATA_PATH):
        print("📂 Loading existing reels dataset...")

        df = pd.read_csv(DATA_PATH)

        # 🔥 FIX: تحديد الفورمات لتجنب warning
        df["created_at"] = pd.to_datetime(
            df["created_at"],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        )

        df = df.dropna(subset=["created_at"])

        return df

    print("⚙️ Generating reels dataset...")

    from src.data.generate_brands import get_brands
    brands_df = get_brands()

    df = generate_reels(brands_df)

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    return df