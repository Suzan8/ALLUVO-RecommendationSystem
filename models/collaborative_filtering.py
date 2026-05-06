import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD


# =========================
# Train CF Model (SAFE)
# =========================
def train_cf(interaction_matrix, n_factors=50):

    # 🔥 حالة البيانات القليلة جدًا
    if interaction_matrix.shape[0] < 2 or interaction_matrix.shape[1] < 2:
        print("⚠️ Not enough data for CF — fallback to zeros")

        return pd.DataFrame(
            np.zeros_like(interaction_matrix),
            index=interaction_matrix.index,
            columns=interaction_matrix.columns
        )

    # 🔥 تأمين n_components (لازم أقل من عدد الأعمدة)
    n_components = min(n_factors, interaction_matrix.shape[1] - 1)

    svd = TruncatedSVD(n_components=n_components, random_state=42)

    user_latent = svd.fit_transform(interaction_matrix)
    item_latent = svd.components_

    predicted_matrix = np.dot(user_latent, item_latent)

    predicted_df = pd.DataFrame(
        predicted_matrix,
        index=interaction_matrix.index,
        columns=interaction_matrix.columns
    )

    # 🔥 إزالة العناصر اللي المستخدم شافها
    already_watched = interaction_matrix > 0
    predicted_df[already_watched] = 0

    return predicted_df


# =========================
# Recommend CF (SAFE)
# =========================
def recommend_cf(predicted_df, user_id, top_k=10):

    # 🔥 لو user مش موجود في CF
    if user_id not in predicted_df.index:
        print(f"⚠️ User {user_id} not in CF model")
        return []

    user_scores = predicted_df.loc[user_id]

    return user_scores.sort_values(ascending=False).head(top_k)