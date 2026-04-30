def recommend(final_scores, reels_df, popularity_score, user_id, interests=None, k=10):

    # (Hybrid)
    if user_id in final_scores.index:
        return (
            final_scores.loc[user_id]
            .sort_values(ascending=False)
            .head(k)
            .index
            .tolist()
        )

    # (Cold Start)
    elif interests is not None and len(interests) > 0:

        
        temp_df = reels_df.copy()

        temp_df['score'] = temp_df['category'].apply(
            lambda x: 1 if x in interests else 0
        )

        return (
            temp_df
            .sort_values(['score', 'total_views'], ascending=False)
            ['reel_id']
            .head(k)
            .tolist()
        )

    # (Popularity)
    else:
        return (
            popularity_score
            .sort_values(ascending=False)
            .head(k)
            .index
            .tolist()
        )