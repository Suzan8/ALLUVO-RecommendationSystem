import pandas as pd
import numpy as np


# =========================
# Time Decay Model
# =========================
def build_time_decay(interactions_df, lambda_=0.05):

    current_time = interactions_df["timestamp"].max()

    df = interactions_df.copy()

    df["days_since"] = (
        current_time - df["timestamp"]
    ).dt.days

    df["time_weight"] = np.exp(-lambda_ * df["days_since"])

    time_decay_score = df.groupby("reel_id")["time_weight"].sum()

    # normalize
    time_decay_score = time_decay_score / time_decay_score.max()

    return time_decay_score