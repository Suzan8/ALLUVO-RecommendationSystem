import pandas as pd
import numpy as np


# =========================
# Normalize
# =========================
def normalize(df):
    return (df - df.min()) / (df.max() - df.min() + 1e-8)


# =========================
# Hybrid Model (FIXED)
# =========================
def build_hybrid_model(
    content_scores,
    cf_scores,
    popularity_score,
    interactions_df,
    time_decay_score,
    weights=(0.4, 0.4, 0.1, 0.1)
):

    # -------------------------
    # Normalize matrices
    # -------------------------
    content_norm = normalize(content_scores)
    cf_norm = normalize(cf_scores)

    # -------------------------
    # Fix popularity (reels level → broadcast correctly)
    # -------------------------
    popularity_score = popularity_score / (popularity_score.max() + 1e-8)

    popularity_matrix = pd.DataFrame(
        np.repeat(
            popularity_score.values.reshape(1, -1),
            content_norm.shape[0],
            axis=0
        ),
        index=content_norm.index,
        columns=content_norm.columns
    )

    # -------------------------
    # Fix time decay (reels level)
    # -------------------------
    time_decay_score = time_decay_score / (time_decay_score.max() + 1e-8)

    time_matrix = pd.DataFrame(
        np.repeat(
            time_decay_score.values.reshape(1, -1),
            content_norm.shape[0],
            axis=0
        ),
        index=content_norm.index,
        columns=content_norm.columns
    )

    # -------------------------
    # Weighted sum
    # -------------------------
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

    if user_id not in final_scores.index:
        return []

    user_scores = final_scores.loc[user_id]

    seen_reels = interactions_df[
        interactions_df["user_id"] == user_id
    ]["reel_id"]

    user_scores = user_scores.drop(seen_reels, errors="ignore")

    return user_scores.sort_values(ascending=False).head(top_k)