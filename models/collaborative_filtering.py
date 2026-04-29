import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD


# =========================
# Train CF Model
# =========================
def train_cf(interaction_matrix, n_factors=50):

    svd = TruncatedSVD(n_components=n_factors, random_state=42)

    user_latent = svd.fit_transform(interaction_matrix)
    item_latent = svd.components_

    predicted_matrix = np.dot(user_latent, item_latent)

    predicted_df = pd.DataFrame(
        predicted_matrix,
        index=interaction_matrix.index,
        columns=interaction_matrix.columns
    )

    # remove already interacted items
    already_watched = interaction_matrix > 0
    predicted_df[already_watched] = 0

    return predicted_df


# =========================
# Recommend CF
# =========================
def recommend_cf(predicted_df, user_id, top_k=10):

    user_scores = predicted_df.loc[user_id]
    return user_scores.sort_values(ascending=False).head(top_k)