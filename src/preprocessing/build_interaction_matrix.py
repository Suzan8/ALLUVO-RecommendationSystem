import pandas as pd
import os


# =========================
# Build Interaction Matrix
# =========================
def build_interaction_matrix(interactions_df):

    interaction_matrix = interactions_df.pivot_table(
        index="user_id",
        columns="reel_id",
        values="watch_ratio",
        fill_value=0
    )

    return interaction_matrix


# =========================
# Save Matrix
# =========================
def save_interaction_matrix(interaction_matrix):

    path = "data/processed/user_item_matrix.csv"

    os.makedirs(os.path.dirname(path), exist_ok=True)
    interaction_matrix.to_csv(path)

    return path


# =========================
# Test
# =========================
if __name__ == "__main__":

    from src.preprocessing.load_data import load_data

    _, _, _, interactions_df = load_data()

    matrix = build_interaction_matrix(interactions_df)

    print(matrix.head())

    save_interaction_matrix(matrix)