import numpy as np


# =========================
# Precision@K
# =========================
def precision_at_k(actual, pred):

    actual = set(actual)

    return len(set(pred) & actual) / len(pred) if len(pred) > 0 else 0


# =========================
# Recall@K
# =========================
def recall_at_k(actual, pred):

    actual = set(actual)

    return len(set(pred) & actual) / len(actual) if len(actual) > 0 else 0


# =========================
# NDCG@K
# =========================
def ndcg_at_k(actual, pred, k=10):

    actual = set(actual)

    dcg = 0
    for i, item in enumerate(pred[:k]):
        if item in actual:
            dcg += 1 / np.log2(i + 2)

    ideal = sum(
        1 / np.log2(i + 2)
        for i in range(min(len(actual), k))
    )

    return dcg / ideal if ideal > 0 else 0