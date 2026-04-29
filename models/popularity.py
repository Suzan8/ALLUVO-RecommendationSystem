import pandas as pd


# =========================
# Build Popularity Model
# =========================
def build_popularity_model(reels_df):

    popularity_score = reels_df.set_index("reel_id")["total_views"]
    popularity_score = popularity_score / popularity_score.max()

    return popularity_score


# =========================
# Top Popular Reels
# =========================
def get_top_popular(popularity_score, top_k=10):

    return popularity_score.sort_values(ascending=False).head(top_k)


# =========================
# Real popularity (for evaluation only)
# =========================
def get_real_popularity(interactions_df, top_k=10):

    real_views = interactions_df.groupby("reel_id")["view"].sum()

    return real_views.sort_values(ascending=False).head(top_k)