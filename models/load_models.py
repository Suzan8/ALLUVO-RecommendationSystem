import joblib


def load_all():

    final_scores = joblib.load("models/final_scores.pkl")
    reels_df = joblib.load("models/reels_df.pkl")
    popularity_score = joblib.load("models/popularity.pkl")

    return final_scores, reels_df, popularity_score