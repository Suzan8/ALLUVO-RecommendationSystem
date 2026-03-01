# src/data/generate_brands.py

import pandas as pd
import numpy as np
import random

np.random.seed(42)

def generate_brands(num_brands=30):
    categories = ["Fashion", "Beauty", "Fitness", "Technology", "Home", "Sports", "Gaming"]

    brands = []

    for i in range(1, num_brands + 1):
        brand = {
            "brand_id": i,
            "brand_name": f"Brand {i}",
            "category": random.choice(categories),
            "brand_popularity_score": round(random.uniform(20, 100), 2)  # رقم واقعي
        }
        brands.append(brand)

    return pd.DataFrame(brands)


if __name__ == "__main__":
    df = generate_brands()
    df.to_csv("data/raw/brands.csv", index=False)
    print("Brands dataset generated successfully.")