import pandas as pd


# =========================
# Level 2: Content-Based Cold Start
# =========================
def cold_start_content(users_df, reels_df, user_id, k=10):

    user = users_df[users_df["user_id"] == user_id]

    if len(user) == 0:
        return popularity_recommendation(None, k)

    interests = user["interests"].values[0]

    scores = reels_df.copy()
    scores["match"] = scores["category"].apply(
        lambda x: 1 if x in interests else 0
    )

    return scores.sort_values("match", ascending=False)["reel_id"].head(k).tolist()


# =========================
# Level 3: Popularity fallback
# =========================
def popularity_recommendation(interactions_df, k=10):

    return (
        interactions_df.groupby("reel_id")["view"]
        .sum()
        .sort_values(ascending=False)
        .head(k)
        .index
        .tolist()
    )


