import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# Build Reel Features
# =========================
def build_reel_features(reels_df):

    encoder = OneHotEncoder()

    reel_category_encoded = encoder.fit_transform(
        reels_df[["category"]]
    ).toarray()

    reel_features = pd.DataFrame(
        reel_category_encoded,
        columns=encoder.get_feature_names_out(["category"]),
        index=reels_df["reel_id"]
    )

    return reel_features


# =========================
# Build User Vectors
# =========================
def build_user_vectors(users_df):

    interest_cols = [
        col for col in users_df.columns
        if col.startswith("interest_")
    ]

    user_vectors = users_df.set_index("user_id")[interest_cols]

    return user_vectors


# =========================
# Compute Similarity Scores
# =========================
def compute_content_scores(user_vectors, reel_features):

    similarity_matrix = cosine_similarity(user_vectors, reel_features)

    content_scores = pd.DataFrame(
        similarity_matrix,
        index=user_vectors.index,
        columns=reel_features.index
    )

    return content_scores


# =========================
# Recommend function
# =========================
def recommend_content(content_scores, user_id, top_k=15):

    return content_scores.loc[user_id].sort_values(ascending=False).head(top_k)