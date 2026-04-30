from fastapi import FastAPI
from typing import Optional, List
from src.utils.helpers import recommend
from models.load_models import load_all

app = FastAPI()


final_scores, reels_df, popularity_score = load_all()


@app.post("/recommend")
def recommend_api(
    user_id: int,
    interests: Optional[List[str]] = None,
    k: int = 10
):

    
    if interests:
        interests = [
            i.strip() for i in interests
            if i and i.strip().lower() != "string"
        ]

        
        if len(interests) == 0:
            interests = None

    recs = recommend(
        final_scores=final_scores,
        reels_df=reels_df,
        popularity_score=popularity_score,
        user_id=user_id,
        interests=interests,
        k=k
    )

    return {
        "user_id": user_id,
        "recommended_reels": recs,
        "model": (
            "hybrid" if user_id in final_scores.index
            else "cold_start" if interests is not None
            else "popularity"
        )
    }