import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# Build unified text space (SAFE VERSION)
# =========================
def build_unified_features(users_df, reels_df):

    # =========================
    # USERS (engineered features only)
    # =========================
    interest_cols = [
        col for col in users_df.columns
        if col.startswith("interest_")
    ]

    if len(interest_cols) == 0:
        users_text = pd.Series([""] * len(users_df))
    else:
        users_text = users_df[interest_cols].astype(str).agg(" ".join, axis=1)

    # =========================
    # REELS (SAFE CATEGORY HANDLING)
    # =========================
    if "category" in reels_df.columns:
        reels_text = reels_df["category"].astype(str)
    else:
        print("⚠️ Warning: 'category' column missing in reels_df. Using fallback.")
        reels_text = pd.Series(["unknown"] * len(reels_df))

    # =========================
    # TF-IDF
    # =========================
    vectorizer = TfidfVectorizer()

    all_text = pd.concat([users_text, reels_text], ignore_index=True)

    tfidf_matrix = vectorizer.fit_transform(all_text)

    user_vectors = tfidf_matrix[:len(users_df)]
    reel_vectors = tfidf_matrix[len(users_df):]

    return (
        user_vectors,
        reel_vectors,
        users_df["user_id"],
        reels_df["reel_id"]
    )


# =========================
# Similarity
# =========================
def compute_content_scores(user_vectors, reel_vectors, user_ids, reel_ids):

    scores = cosine_similarity(user_vectors, reel_vectors)

    return pd.DataFrame(
        scores,
        index=user_ids,
        columns=reel_ids
    )


# =========================
# Recommend function
# =========================
def recommend_content(content_scores, user_id, top_k=15):

    if user_id not in content_scores.index:
        return []

    return content_scores.loc[user_id] \
        .sort_values(ascending=False) \
        .head(top_k)