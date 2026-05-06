import time

from src.preprocessing.load_data import load_data
from src.preprocessing.feature_engineering import feature_engineering
from src.preprocessing.build_interaction_matrix import build_interaction_matrix

from models.content_based import (
    build_unified_features,
    compute_content_scores
)

from models.collaborative_filtering import train_cf
from models.popularity import build_popularity_model
from models.time_decay import build_time_decay
from models.hybrid import build_hybrid_model

from models.save_models import save_all


# =========================
# Full retrain pipeline
# =========================
def retrain():

    print(" Retraining started...")

    # 1. Load data
    users_df, brands_df, reels_df, interactions_df = load_data()

    # 2. Feature Engineering
    users_df, reels_df = feature_engineering(
        users_df, reels_df, interactions_df
    )

    # 3. Interaction Matrix
    interaction_matrix = build_interaction_matrix(interactions_df, reels_df)

    # 4. Content-Based (FIXED PIPELINE)
    user_vectors, reel_vectors, user_ids, reel_ids = build_unified_features(
        users_df, reels_df
    )

    content_scores = compute_content_scores(
        user_vectors,
        reel_vectors,
        user_ids,
        reel_ids
    )

    # 5. CF Model
    cf_scores = train_cf(interaction_matrix)

    # 6. Popularity Model
    popularity_score = build_popularity_model(reels_df)

    # 7. Time Decay Model
    time_decay_score = build_time_decay(interactions_df, reels_df)

    # 8. Hybrid Model
    final_scores = build_hybrid_model(
        content_scores,
        cf_scores,
        popularity_score,
        interactions_df,
        time_decay_score
    )

    # 9. Save Models
    save_all(final_scores, reels_df, popularity_score)

    print("✅ Retraining finished!")


# =========================
# Loop every hour
# =========================
def retrain_loop(interval=60):  # 3600 = 1 hour

    while True:
        try:
            retrain()
        except Exception as e:
            print("❌ Error in retraining:", e)

        print(f" Waiting {interval} seconds...")
        time.sleep(interval)


# =========================
# Run directly
# =========================
if __name__ == "__main__":
    retrain_loop(interval=60)