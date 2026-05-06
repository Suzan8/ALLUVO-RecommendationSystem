import pandas as pd
import json

from src.data.generate_users import get_users
from src.data.generate_brands import get_brands
from src.data.generate_reels import get_reels
from src.data.generate_interactions import get_interactions


# =========================
# Load + Preprocess Users
# =========================
def preprocess_users(users_df: pd.DataFrame):

    users_df = users_df.copy()

    # -------------------------
    # JSON fields fix (SAFE)
    # -------------------------
    users_df["interests"] = users_df["interests"].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )

    users_df["followed_brands"] = users_df["followed_brands"].apply(
        lambda x: json.loads(x) if isinstance(x, str) else x
    )

    # -------------------------
    # Gender Encoding
    # -------------------------
    if "gender" in users_df.columns:
        users_df["gender"] = users_df["gender"].fillna("Unknown")
        users_df = pd.get_dummies(users_df, columns=["gender"])

    # -------------------------
    # Interests text (optional)
    # -------------------------
    users_df["interests_str"] = users_df["interests"].apply(
        lambda x: ",".join(x) if isinstance(x, list) else ""
    )

    return users_df


# =========================
# Load all datasets
# =========================
def load_data():

    # 🟢 load / generate
    users_df = get_users()
    brands_df = get_brands()
    reels_df = get_reels()
    interactions_df = get_interactions()

    # =========================
    # 🔥 IMPORTANT: Fix TYPES
    # =========================
    users_df["user_id"] = users_df["user_id"].astype(int)
    reels_df["reel_id"] = reels_df["reel_id"].astype(int)
    reels_df["brand_id"] = reels_df["brand_id"].astype(int)

    interactions_df["user_id"] = interactions_df["user_id"].astype(int)
    interactions_df["reel_id"] = interactions_df["reel_id"].astype(int)

    # =========================
    # Preprocess USERS
    # =========================
    users_df = preprocess_users(users_df)

    # =========================
    # Datetime parsing (FIX ALL FORMATS)
    # =========================
    users_df["created_at"] = pd.to_datetime(
        users_df["created_at"],
        errors="coerce"
    )

    reels_df["created_at"] = pd.to_datetime(
        reels_df["created_at"],
        errors="coerce"
    )

    interactions_df["timestamp"] = pd.to_datetime(
        interactions_df["timestamp"],
        errors="coerce"
    )

    # =========================
    # 🔥 DROP BAD ROWS (VERY IMPORTANT)
    # =========================
    # users_df = users_df.dropna(subset=["created_at"])
    #reels_df = reels_df.dropna(subset=["created_at"])
    #interactions_df = interactions_df.dropna(subset=["timestamp"])

    # =========================
    # 🔥 REMOVE DUPLICATES (UPSERT SAFETY)
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

    print("🔍 Check user 9999 exists:", 9999 in users_df["user_id"].values)
    print("🔍 Check interaction exists:", 9999 in interactions_df["user_id"].values)

    return users_df, brands_df, reels_df, interactions_df


# =========================
# Test
# =========================
if __name__ == "__main__":
    users_df, brands_df, reels_df, interactions_df = load_data()

    print(users_df.head())
    print(reels_df.head())
    print(interactions_df.head())