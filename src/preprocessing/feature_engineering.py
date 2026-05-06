import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


# =========================
# Feature Engineering (FINAL STABLE VERSION)
# =========================
def feature_engineering(users_df, reels_df, interactions_df):

    users_df = users_df.copy()
    reels_df = reels_df.copy()

    # =========================
    # 1. Gender Encoding
    # =========================
    if "gender" in users_df.columns:
        users_df["gender"] = users_df["gender"].fillna("Unknown")
        users_df = pd.get_dummies(users_df, columns=["gender"], drop_first=False)

    # =========================
    # 2. Interests Encoding (SAFE)
    # =========================
    if "interests" in users_df.columns:

        users_df["interests"] = users_df["interests"].apply(
            lambda x: x if isinstance(x, list) else []
        )

        mlb = MultiLabelBinarizer()

        interest_features = pd.DataFrame(
            mlb.fit_transform(users_df["interests"]),
            columns=[f"interest_{c}" for c in mlb.classes_],
            index=users_df.index
        )

        users_df = pd.concat([users_df, interest_features], axis=1)
        users_df.drop(columns=["interests"], inplace=True, errors="ignore")

    # =========================
    # 3. Followed Brands Encoding
    # =========================
    if "followed_brands" in users_df.columns:

        users_df["followed_brands"] = users_df["followed_brands"].apply(
            lambda x: x if isinstance(x, list) else []
        )

        mlb2 = MultiLabelBinarizer()

        brand_features = pd.DataFrame(
            mlb2.fit_transform(users_df["followed_brands"]),
            columns=[f"brand_{c}" for c in mlb2.classes_],
            index=users_df.index
        )

        users_df = pd.concat([users_df, brand_features], axis=1)
        users_df.drop(columns=["followed_brands"], inplace=True, errors="ignore")

    # =========================
    # 4. created_at handling (SAFE)
    # =========================
    if "created_at" in users_df.columns:

        users_df["created_at"] = pd.to_datetime(
            users_df["created_at"],
            errors="coerce"
        )

        users_df["account_age_days"] = (
            pd.Timestamp.now() - users_df["created_at"]
        ).dt.days

        users_df["account_year"] = users_df["created_at"].dt.year
        users_df["account_month"] = users_df["created_at"].dt.month

        users_df.drop(columns=["created_at"], inplace=True, errors="ignore")

    # =========================
    # 5. Interaction Features
    # =========================
    if "user_id" in interactions_df.columns:

        user_interactions = interactions_df.groupby("user_id").size()

        users_df = users_df.merge(
            user_interactions.rename("total_interactions"),
            on="user_id",
            how="left"
        )

        users_df["total_interactions"] = users_df["total_interactions"].fillna(0)

    # =========================
    # 6. Reel Features
    # =========================
    if "reel_id" in interactions_df.columns:

        if "view" in interactions_df.columns:
            reel_views = interactions_df.groupby("reel_id")["view"].sum()
        else:
            reel_views = interactions_df.groupby("reel_id").size()

        reels_df = reels_df.merge(
            reel_views.rename("total_views"),
            on="reel_id",
            how="left"
        )

        reels_df["total_views"] = reels_df["total_views"].fillna(0)

    # =========================
    # 7. FINAL CLEANING (IMPORTANT FIX)
    # =========================
    users_df = users_df.fillna(0)
    reels_df = reels_df.fillna(0)

    # ❌ DO NOT keep raw object columns
    users_df = users_df.select_dtypes(include=["number"])

    # خليه يحتفظ بالـ category
    reels_numeric = reels_df.select_dtypes(include=["number"])

    if "category" in reels_df.columns:
         reels_numeric["category"] = reels_df["category"]

    reels_df = reels_numeric
    

    return users_df, reels_df


# =========================
# Test
# =========================
if __name__ == "__main__":

    from src.preprocessing.load_data import load_data

    users_df, brands_df, reels_df, interactions_df = load_data()

    users_df, reels_df = feature_engineering(users_df, reels_df, interactions_df)

    print("Users shape:", users_df.shape)
    print(users_df.head())

    print("Reels shape:", reels_df.shape)
    print(reels_df.head())