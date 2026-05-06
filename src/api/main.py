from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel
import pandas as pd
import json
import os


from src.utils.helpers import (
    recommend,
    upsert_data,
    update_after_interaction,
    replace_reel_in_model
)

from models.load_models import load_all

app = FastAPI()


# ==============================
# Load models
# ==============================
def get_models():
    return load_all()


# ==============================
# Schemas
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
# Recommendation
# ==============================
@app.post("/recommend")
def recommend_api(user_id: int, interests: Optional[List[str]] = None, k: int = 10):

    if interests:
        interests = [i.strip() for i in interests if i and i != "string"]
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
        "recommended_reels": list(recs),
        "model": (
            "hybrid" if user_id in final_scores.index
            else "cold_start" if interests
            else "popularity"
        )
    }


# ==============================
# Add User
# ==============================
@app.post("/add_user")
def add_user(user: User):

    file_path = "data/raw/users.csv"
    

    data = user.dict()

    data["interests"] = json.dumps(data["interests"])
    data["followed_brands"] = json.dumps(data["followed_brands"])

    df = pd.DataFrame([data])
    upsert_data(file_path, df, "user_id")

    return {"message": "User added"}


# ==============================
# Add Reel
# ==============================
@app.post("/add_reel")
def add_reel(reel: Reel):

    df = pd.DataFrame([reel.dict()])
    upsert_data("data/raw/reels.csv", df, "reel_id")

    return {"message": "Reel added"}


# ==============================
# Add Brand
# ==============================
@app.post("/add_brand")
def add_brand(brand: Brand):

    df = pd.DataFrame([brand.dict()])
    upsert_data("data/raw/brands.csv", df, "brand_id")

    return {"message": "Brand added"}


# ==============================
# Add Interaction
# ==============================
@app.post("/add_interaction")
def add_interaction(interaction: Interaction):

    data = interaction.dict()

    # 🔥 تأكد فورمات timestamp
    data["timestamp"] = pd.to_datetime(
        data["timestamp"],
        errors="coerce"
    )

    if pd.isna(data["timestamp"]):
        return {"error": "Invalid timestamp format"}

    # رجعه string موحد
    data["timestamp"] = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([data])

    upsert_data("data/raw/interactions.csv", df, ["user_id", "reel_id"])

    return {"message": "Interaction added"}