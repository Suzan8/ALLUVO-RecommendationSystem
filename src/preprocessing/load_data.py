import pandas as pd
import json
import os


# =========================
# Safe JSON loader
# =========================
def safe_json_load(x):
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        try:
            return json.loads(x)
        except:
            return []
    return []


# =========================
# 🔥 FIX: multi-format datetime parser
# =========================
def parse_datetime_column(col):
    dt1 = pd.to_datetime(col, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    dt2 = pd.to_datetime(col, format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    return dt1.fillna(dt2)


# =========================
# Preprocess Users
# =========================
def preprocess_users(users_df: pd.DataFrame):

    users_df = users_df.copy()

    # JSON fix
    if "interests" in users_df.columns:
        users_df["interests"] = users_df["interests"].apply(safe_json_load)

    if "followed_brands" in users_df.columns:
        users_df["followed_brands"] = users_df["followed_brands"].apply(safe_json_load)

    # Gender encoding
    if "gender" in users_df.columns:
        users_df["gender"] = users_df["gender"].fillna("Unknown")
        users_df = pd.get_dummies(users_df, columns=["gender"])

    # Interests text
    if "interests" in users_df.columns:
        users_df["interests_str"] = users_df["interests"].apply(
            lambda x: ",".join(x) if isinstance(x, list) else ""
        )

    return users_df


# =========================
# Load all datasets (NO GENERATION)
# =========================
def load_data():

    users_df = pd.read_csv("data/raw/users.csv")
    brands_df = pd.read_csv("data/raw/brands.csv")
    reels_df = pd.read_csv("data/raw/reels.csv")
    interactions_df = pd.read_csv("data/raw/interactions.csv")

    # =========================
    # FIX TYPES
    # =========================
    users_df["user_id"] = pd.to_numeric(users_df["user_id"], errors="coerce")
    reels_df["reel_id"] = pd.to_numeric(reels_df["reel_id"], errors="coerce")
    reels_df["brand_id"] = pd.to_numeric(reels_df["brand_id"], errors="coerce")

    interactions_df["user_id"] = pd.to_numeric(interactions_df["user_id"], errors="coerce")
    interactions_df["reel_id"] = pd.to_numeric(interactions_df["reel_id"], errors="coerce")

    users_df = users_df.dropna(subset=["user_id"])
    reels_df = reels_df.dropna(subset=["reel_id"])
    interactions_df = interactions_df.dropna(subset=["user_id", "reel_id"])

    users_df["user_id"] = users_df["user_id"].astype(int)
    reels_df["reel_id"] = reels_df["reel_id"].astype(int)
    reels_df["brand_id"] = reels_df["brand_id"].astype(int)

    interactions_df["user_id"] = interactions_df["user_id"].astype(int)
    interactions_df["reel_id"] = interactions_df["reel_id"].astype(int)

    # =========================
    # preprocess users
    # =========================
    users_df = preprocess_users(users_df)

    # =========================
    # 🔥 FIX datetime (multi-format)
    # =========================
    users_df["created_at"] = parse_datetime_column(users_df["created_at"])
    reels_df["created_at"] = parse_datetime_column(reels_df["created_at"])
    interactions_df["timestamp"] = parse_datetime_column(interactions_df["timestamp"])

    # ❗ مهم: سيب users زي ما هو
    reels_df = reels_df.dropna(subset=["created_at"])
    interactions_df = interactions_df.dropna(subset=["timestamp"])

    # =========================
    # remove duplicates
    # =========================
    users_df = users_df.drop_duplicates(subset=["user_id"], keep="last")
    reels_df = reels_df.drop_duplicates(subset=["reel_id"], keep="last")
    brands_df = brands_df.drop_duplicates(subset=["brand_id"], keep="last")

    interactions_df = interactions_df.drop_duplicates(
        subset=["user_id", "reel_id"],
        keep="last"
    )

    # =========================
    # DEBUG
    # =========================
    print("✅ Users:", users_df.shape)
    print("✅ Reels:", reels_df.shape)
    print("✅ Interactions:", interactions_df.shape)
    print("✅ brands:", brands_df.shape)


    return users_df, brands_df, reels_df, interactions_df