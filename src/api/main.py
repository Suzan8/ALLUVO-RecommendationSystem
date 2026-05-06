from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel
import pandas as pd
import json

from src.utils.helpers import (
    recommend,
    upsert_data,
    update_after_interaction,
    replace_reel_in_model
)

from models.load_models import load_all

app = FastAPI()


# ==============================
# 🔹 Load models (dynamic)
# ==============================
def get_models():
    return load_all()


# ==============================
# 🔹 Schemas
# ==============================
class User(BaseModel):
    user_id: int
    age: int
    gender: str
    interests: List[str]
    followed_brands: List[int]
    created_at: str


class Reel(BaseModel):
    reel_id: int
    brand_id: int
    category: str
    price: float
    created_at: str
    video_duration: int


class Interaction(BaseModel):
    user_id: int
    reel_id: int
    view: int
    watch_ratio: float
    like: int
    comment: int
    purchase: int
    timestamp: str


class Brand(BaseModel):
    brand_id: int
    brand_name: str
    category: str
    brand_popularity_score: float


# ==============================
# 🔹 Recommendation
# ==============================
@app.post("/recommend")
def recommend_api(user_id: int, interests: Optional[List[str]] = None, k: int = 10):
    if interests:
        interests = [
            i.strip() for i in interests
            if i and i.strip().lower() != "string"
        ]

        
        if len(interests) == 0:
            interests = None

            
    final_scores, reels_df, popularity_score = get_models()

    recs = recommend(
        final_scores,
        reels_df,
        popularity_score,
        user_id,
        interests,
        k
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


# ==============================
# 🔹 Add User
# ==============================

@app.post("/add_user")
def add_user(user: User):

    data = user.dict()

    data["interests"] = json.dumps(data["interests"])
    data["followed_brands"] = json.dumps(data["followed_brands"])

    df = pd.DataFrame([data])
    upsert_data("data/raw/users.csv", df, "user_id")

    return {"message": "User added"}
# ==============================
# 🔹 Add Reel
# ==============================
@app.post("/add_reel")
def add_reel(reel: Reel):

    final_scores, reels_df, popularity_score = get_models()

    df = pd.DataFrame([reel.dict()])
    upsert_data("data/raw/reels.csv", df, "reel_id")

    final_scores = replace_reel_in_model(final_scores, reel.reel_id)

    return {"message": "Reel updated"}


# ==============================
# 🔹 Add Brand
# ==============================
@app.post("/add_brand")
def add_brand(brand: Brand):

    df = pd.DataFrame([brand.dict()])
    upsert_data("data/raw/brands.csv", df, "brand_id")

    return {"message": "Brand added"}


# ==============================
# 🔹 Add Interaction
# ==============================
@app.post("/add_interaction")
def add_interaction(interaction: Interaction):

    final_scores, reels_df, popularity_score = get_models()

    df = pd.DataFrame([interaction.dict()])
    upsert_data("data/raw/interactions.csv", df, ["user_id", "reel_id"])

    final_scores, popularity_score = update_after_interaction(
        final_scores,
        popularity_score,
        interaction
    )

    return {"message": "Interaction added"}