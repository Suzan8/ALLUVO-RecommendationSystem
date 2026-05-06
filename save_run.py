from src.preprocessing.load_data import load_data
from src.preprocessing.feature_engineering import feature_engineering
from src.preprocessing.build_interaction_matrix import build_interaction_matrix

from models.content_based import (
    build_reel_features,
    build_user_vectors,
    compute_content_scores
)

from models.collaborative_filtering import train_cf
from models.popularity import build_popularity_model
from models.time_decay import build_time_decay
from models.hybrid import build_hybrid_model

from models.save_models import save_all


# =========================
# Load Data
# =========================
users_df, brands_df, reels_df, interactions_df = load_data()

# =========================
# Feature Engineering
# =========================
users_df, reels_df = feature_engineering(users_df, reels_df, interactions_df)

# =========================
# Interaction Matrix
# =========================
interaction_matrix = build_interaction_matrix(interactions_df)

# =========================
# 🔥 Content-Based Model (manual build)
# =========================
reel_features = build_reel_features(reels_df)
user_vectors = build_user_vectors(users_df)
content_scores = compute_content_scores(user_vectors, reel_features)

# =========================
# CF Model
# =========================
cf_scores = train_cf(interaction_matrix)

# =========================
# Popularity
# =========================
popularity_score = build_popularity_model(reels_df)

# =========================
# Time Decay
# =========================
time_decay_score = build_time_decay(interactions_df)

# =========================
# Hybrid
# =========================
final_scores = build_hybrid_model(
    content_scores,
    cf_scores,
    popularity_score,
    interactions_df,
    time_decay_score
)

# =========================
# Save
# =========================
save_all(final_scores, reels_df, popularity_score)

print("✅ Models saved successfully!")