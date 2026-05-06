import pandas as pd
import numpy as np

# ==============================
# 🔹 UPSERT (Replace)
# ==============================
def upsert_data(file_path, new_df, key_col):

    try:
        old_df = pd.read_csv(file_path)

        if isinstance(key_col, list):
            mask = pd.Series(True, index=old_df.index)
            for col in key_col:
                mask &= ~old_df[col].isin(new_df[col])
            old_df = old_df[mask]
        else:
            old_df = old_df[~old_df[key_col].isin(new_df[key_col])]

        combined = pd.concat([old_df, new_df], ignore_index=True)

    except FileNotFoundError:
        combined = new_df

    # 🔥 FIX مهم
    combined = combined.reset_index(drop=True)

    combined.to_csv(file_path, index=False)


# ==============================
# 🔹 Recommendation
# ==============================
def recommend(final_scores, reels_df, popularity_score, user_id, interests=None, k=10):

    # 🟢 Hybrid
    if final_scores is not None and user_id in final_scores.index:
        user_scores = final_scores.loc[user_id]

        if user_scores.sum() > 0:
            return (
                user_scores
                .sort_values(ascending=False)
                .head(k)
                .index
                .tolist()
            )

    # 🟡 Cold Start
    if interests:
        temp_df = reels_df.copy()

        temp_df["score"] = temp_df["category"].apply(
            lambda x: 1 if x in interests else 0
        )

        return (
            temp_df
            .sort_values(["score", "total_views"], ascending=False)
            ["reel_id"]
            .head(k)
            .tolist()
        )

    # 🔵 Popularity
    return (
        popularity_score
        .sort_values(ascending=False)
        .head(k)
        .index
        .tolist()
    )


# ==============================
# 🔹 Replace Reel
# ==============================
def replace_reel_in_model(final_scores, reel_id):

    if reel_id in final_scores.columns:
        final_scores.drop(columns=[reel_id], inplace=True)

    final_scores[reel_id] = 0

    return final_scores


# ==============================
# 🔹 Interaction Update (Light realtime)
# ==============================
def update_after_interaction(final_scores, popularity_score, interaction):

    user_id = interaction.user_id
    reel_id = interaction.reel_id

    # user
    if user_id not in final_scores.index:
        final_scores.loc[user_id] = 0

    # reel
    if reel_id not in final_scores.columns:
        final_scores[reel_id] = 0

    # learning
    final_scores.loc[user_id, reel_id] += 1

    # popularity
    if reel_id in popularity_score.index:
        popularity_score[reel_id] += 1
    else:
        popularity_score[reel_id] = 1

    popularity_score = popularity_score / popularity_score.max()

    return final_scores, popularity_score