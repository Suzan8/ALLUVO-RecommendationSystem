# Alluvo Hybrid Recommendation System

A Hybrid Recommendation System built for Alluvo, a brand-based reels platform where users interact with product videos through likes, comments, views, and purchases.

---

## 🚀 Project Goal

To build a scalable Hybrid Recommendation System that combines:

- Content-Based Filtering (interests, categories, followed brands)
- Collaborative Filtering (interaction matrix)
- Popularity Boosting
- Time Decay Ranking

---

## 📊 Dataset (Synthetic)

Since the platform is in development stage, we generate realistic synthetic data including:

- Users
- Brands
- Reels (Products as short videos)
- User-Reel Interactions

The dataset simulates:
- Watch ratio behavior
- Likes and comments probability
- Purchase likelihood
- Cold-start users
- Popular vs. niche brands

---

## 🏗 Project Structure

ALLUVO-RecommendationSystem/
│
├── RS_env/
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
│
├── notebooks/
│
├── src/
│   ├── data/
│   │   ├── generate_users.py
│   │   ├── generate_brands.py
│   │   ├── generate_reels.py
│   │   └── generate_interactions.py
│   │
│   ├── preprocessing/
│   │   ├── build_interaction_matrix.py
│   │   └── feature_engineering.py
│   │
│   ├── models/
│   │   ├── content_based.py
│   │   ├── collaborative_filtering.py
│   │   ├── popularity.py
│   │   ├── time_decay.py
│   │   └── hybrid.py
│   │
│   ├── evaluation/
│   │   └── metrics.py
│   │
│   └── utils/
│       └── helpers.py
│
├── requirements.txt
├── README.md
└── .gitignore

---
🧠 Recommendation Strategy

Generate synthetic data

Build user-item interaction matrix

Apply:

Content Similarity

Matrix Factorization

Popularity Adjustment

Time Decay

Rank and serve top-N recommendations




## ⚙️ Setup

```bash
python -m venv RS_env
source RS_env/bin/activate  # Mac/Linux
RS_env\Scripts\activate     # Windows

pip install -r requirements.txt

