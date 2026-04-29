# =========================
# Main Recommendation Router
# =========================
def recommend(
    user_id,
    final_scores,
    users_df,
    reels_df,
    interactions_df,
    k=10
):

    # Level 1: Normal model
    if final_scores is not None and user_id in final_scores.index:
        return final_scores.loc[user_id] \
            .sort_values(ascending=False) \
            .head(k) \
            .index \
            .tolist()

    # Level 2: Content-based cold start
    elif user_id in users_df["user_id"].values:
        from models.cold_start import cold_start_content
        return cold_start_content(users_df, reels_df, user_id, k)

    # Level 3: Popularity fallback
    else:
        from models.cold_start import popularity_recommendation
        return popularity_recommendation(interactions_df, k)