import numpy as np
import pandas as pd


def build_time_decay(interactions_df, reels_df, lambda_=0.05):

    # لو مفيش interactions
    if interactions_df.empty:
        return pd.Series(0, index=reels_df["reel_id"])

    current_time = interactions_df["timestamp"].max()

    df = interactions_df.copy()

    df["days_since"] = (
        current_time - df["timestamp"]
    ).dt.days

    df["time_weight"] = np.exp(-lambda_ * df["days_since"])

    # 👇 scores حسب reels اللي فيها interaction
    time_decay_score = df.groupby("reel_id")["time_weight"].sum()

    # 🔥 أهم خطوة: ضيف كل reels
    time_decay_score = time_decay_score.reindex(
        reels_df["reel_id"],
        fill_value=0
    )

    # normalize
    if time_decay_score.max() != 0:
        time_decay_score = time_decay_score / time_decay_score.max()

    return time_decay_score