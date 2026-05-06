# Alluvo Hybrid Recommendation System

A Production-ready Hybrid Recommendation System built for Alluvo, a reels-based e-commerce platform.

---

## 🚀 Project Goal

To build a scalable recommendation engine that serves personalized reels using:

- Content-Based Filtering (user interests, categories)
- Collaborative Filtering (user behavior)
- Popularity Boosting
- Time Decay Ranking

---

## 🧠 Recommendation Logic

The system dynamically selects the recommendation strategy:

| Case | Strategy |
|------|--------|
| 🟢 Existing User | Hybrid Model |
| 🟡 New User + Interests | Content-Based (Cold Start) |
| 🔵 New User (No Data) | Popularity |

---

## 📊 Dataset (Synthetic)

Since the platform is still under development, we simulate realistic data:

- Users (age, gender, interests, followed brands)
- Brands (category, popularity)
- Reels (products as videos)
- Interactions (views, likes, comments, purchases)

---

## 🏗 Project Structure
ALLUVO-RecommendationSystem/
│
├── data/
│ ├── raw/
│ ├── processed/
│
├── notebooks/
│
├── src/
│   ├── data/
│   │   ├── generate_users.py
│   │   ├── generate_brands.py
│   │   ├── generate_reels.py
│   │   └── generate_interactions.py
│   ├── preprocessing/
│   │   ├── build_interaction_matrix.py
│   │   ├── feature_engineering.py
│   │   └── load_data.py
│   ├── evaluation/
│   │   ├── evaluation.py
│   │   └── metrics.py
│   ├── utils/
│   │   └── helpers.py
│   ├── pipeline/
│   │   └── retrain.py
│   ├── api/ 
│   │   └── main.py
│
├── models/ 
│   ├── content_based.py
│   ├── collaborative_filtering.py
│   ├── cold_start.py
│   ├── load_models.py
│   ├── save_models.py
│   ├── popularity.py
│   ├── time_decay.py
│   └── hybrid.py
│
├── save_run.py
│
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Setup

```bash
python -m venv RS_env
source RS_env/bin/activate      # Mac/Linux
RS_env\Scripts\activate         # Windows

pip install -r requirements.txt


💾 Save Models
Before running the API, make sure to save trained models:

from save_models import save_all
save_all(final_scores, reels_df, popularity_score)


🚀 Run API
uvicorn src.api.main:app --reload


📡 API Usage
🔹 Endpoint
POST /recommend


🧪 Evaluation
We evaluate the system using:
Precision@K
Recall@K
NDCG@K
Both:
Item-level evaluation
Category-level evaluation (to handle cold start)


🔄 System Flow
User Request
    ↓
API (FastAPI)
    ↓
Recommendation Router
    ↓
Hybrid / Content / Popularity
    ↓
Top-K Reel IDs



