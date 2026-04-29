import joblib
import os


def save_all(final_scores, reels_df, popularity_score):

    os.makedirs("models", exist_ok=True)

    joblib.dump(final_scores, "models/final_scores.pkl")
    joblib.dump(reels_df, "models/reels_df.pkl")
    joblib.dump(popularity_score, "models/popularity.pkl")