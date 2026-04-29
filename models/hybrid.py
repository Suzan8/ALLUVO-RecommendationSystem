import pandas as pd
import numpy as np


# =========================
# Normalize function
# =========================
def normalize(df):
    return (df - df.min()) / (df.max() - df.min())


# =========================
# Build Hybrid Model
# =========================
def build_hybrid_model(
    content_scores,
    cf_scores,
    popularity_score,
    interactions_df,
    time_decay_score,
    weights=(0.35, 0.45, 0.1, 0.1)
):

    content_norm = normalize(content_scores)
    cf_norm = normalize(cf_scores)

    popularity_norm = popularity_score / popularity_score.max()

    # expand popularity to matrix
    popularity_matrix = pd.DataFrame(
        np.tile(popularity_norm.values, (content_norm.shape[0], 1)),
        index=content_norm.index,
        columns=content_norm.columns
    )

    # expand time decay to matrix
    time_decay_score = time_decay_score / time_decay_score.max()

    time_matrix = pd.DataFrame(
        np.tile(time_decay_score.values, (content_norm.shape[0], 1)),
        index=content_norm.index,
        columns=content_norm.columns
    )

    w1, w2, w3, w4 = weights

    final_scores = (
        w1 * content_norm +
        w2 * cf_norm +
        w3 * popularity_matrix +
        w4 * time_matrix
    )

    return final_scores


# =========================
# Recommend function
# =========================
def recommend_hybrid(final_scores, interactions_df, user_id, top_k=10):

    user_scores = final_scores.loc[user_id]

    seen_reels = interactions_df[
        interactions_df["user_id"] == user_id
    ]["reel_id"]

    user_scores = user_scores.drop(seen_reels, errors="ignore")

    return user_scores.sort_values(ascending=False).head(top_k)