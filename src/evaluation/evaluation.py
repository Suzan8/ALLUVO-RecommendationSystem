from sklearn.model_selection import train_test_split


# =========================
# Train / Test Split
# =========================
def split_data(interactions_df):

    train_df, test_df = train_test_split(
        interactions_df,
        test_size=0.2,
        random_state=42
    )

    return train_df, test_df


# =========================
# Actual categories
# =========================
def get_actual_categories(test_df, reels_df, user_id):

    reels = test_df[test_df["user_id"] == user_id]["reel_id"]

    return reels_df[reels_df["reel_id"].isin(reels)]["category"].tolist()


# =========================
# Recommend basic
# =========================
def recommend_reels(final_scores, user_id, k=10):

    return (
        final_scores.loc[user_id]
        .sort_values(ascending=False)
        .head(k)
        .index
        .tolist()
    )


# =========================
# Unique category recommendation
# =========================
def unique_category_recommendations(final_scores, reels_df, user_id, k=10):

    user_scores = final_scores.loc[user_id].sort_values(ascending=False)

    selected_reels = []
    seen_categories = set()

    for reel_id in user_scores.index:

        cat = reels_df.loc[
            reels_df["reel_id"] == reel_id, "category"
        ].values[0]

        if cat not in seen_categories:
            selected_reels.append(reel_id)
            seen_categories.add(cat)

        if len(selected_reels) == k:
            break

    return selected_reels


# =========================
# Predicted categories
# =========================
def get_predicted_categories(final_scores, reels_df, user_id, k=10):

    reels = unique_category_recommendations(final_scores, reels_df, user_id, k)

    return reels_df[reels_df["reel_id"].isin(reels)]["category"].tolist()