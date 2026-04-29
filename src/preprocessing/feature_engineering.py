import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer


# =========================
# Feature Engineering
# =========================
def feature_engineering(users_df, reels_df, interactions_df):

    # =========================
    # User interests encoding
    # =========================
    mlb = MultiLabelBinarizer()

    user_interests = pd.DataFrame(
        mlb.fit_transform(users_df["interests"]),
        columns=[f"interest_{c}" for c in mlb.classes_],
        index=users_df.index
    )

    users_df = pd.concat([users_df, user_interests], axis=1)

    # =========================
    # Total interactions per user
    # =========================
    user_interactions_count = (
        interactions_df.groupby("user_id")
        .size()
        .rename("total_interactions")
    )

    users_df = users_df.merge(user_interactions_count, on="user_id", how="left").fillna(0)

    # =========================
    # Total views per reel
    # =========================
    reel_views_count = (
        interactions_df.groupby("reel_id")["view"]
        .sum()
        .rename("total_views")
    )

    reels_df = reels_df.merge(reel_views_count, on="reel_id", how="left").fillna(0)

    return users_df, reels_df


# =========================
# Test
# =========================
if __name__ == "__main__":

    from src.preprocessing.load_data import load_data

    users_df, brands_df, reels_df, interactions_df = load_data()

    users_df, reels_df = feature_engineering(users_df, reels_df, interactions_df)

    print(users_df.head())
    print(reels_df.head())