import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)

DATA_PATH = "data/raw/brands.csv"

num_brands = 30

categories = ["Fashion","Beauty","Fitness","Technology","Home","Sports","Gaming"]


# =========================
# Core generator (NO CHANGE)
# =========================
def generate_brands():

    brands = []

    for i in range(1, num_brands + 1):
        brand = {
            "brand_id": i,
            "brand_name": f"Brand {i}",
            "category": random.choice(categories),
            "brand_popularity_score": round(random.uniform(20, 100), 2)
        }
        brands.append(brand)

    return pd.DataFrame(brands)


# =========================
# Smart loader
# =========================
def get_brands():

    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)

    df = generate_brands()

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    return df