from fastapi import FastAPI
from src.utils.helpers import recommend
from models.load_models import load_all

app = FastAPI()

# load models once
final_scores, reels_df, popularity_score = load_all()


@app.post("/recommend")
def recommend_api(user_id: int, k: int = 10):

    recs = recommend(
        user_id=user_id,
        final_scores=final_scores,
        users_df=None,
        reels_df=reels_df,
        interactions_df=None,
        k=k
    )

    return {
        "user_id": user_id,
        "recommended_reels": recs
    }