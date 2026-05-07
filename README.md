Alluvo Hybrid Recommendation System
A production-ready Hybrid Recommendation System built for Alluvo, a reels-based e-commerce platform that delivers personalized product reels to users.

Project Overview
This system provides personalized reel recommendations using a combination of:
Content-Based Filtering
Collaborative Filtering
Popularity Ranking
Time Decay Scoring

The project is designed with a scalable architecture suitable for real-world deployment using FastAPI and automatic retraining pipelines.

Recommendation Strategies
The recommendation engine dynamically selects the best strategy depending on the user state.
User State	Recommendation Strategy:
-Existing User with interactions	Hybrid Recommendation
-New User with interests	Cold Start Content-Based
-Completely New User	Popularity-Based Recommendation
-Hybrid Recommendation Formula

Final recommendation scores are generated using:
Final Score =
0.4 × Content-Based Score
+ 0.4 × Collaborative Filtering Score
+ 0.1 × Popularity Score
+ 0.1 × Time Decay Score

Synthetic Dataset
Since the platform is under development, realistic synthetic data is generated automatically.

Users
Age
Gender
Interests
Followed Brands
Account Creation Date
Brands
Brand Name
Category
Popularity Score
Reels
Product Reels
Category
Price
Video Duration
Creation Time
Interactions
Views
Watch Ratio
Likes
Comments
Purchases
Interaction Timestamp

Project Structure
ALLUVO-RecommendationSystem/
│
├── data/
│   ├── raw/
│   └── processed/
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
│   │   ├── load_data.py
│   │   ├── feature_engineering.py
│   │   └── build_interaction_matrix.py
│   │
│   ├── evaluation/
│   │   ├── evaluation.py
│   │   └── metrics.py
│   │
│   ├── utils/
│   │   └── helpers.py
│   │
│   ├── pipeline/
│   │   └── retrain.py
│   │
│   └── api/
│       └── main.py
│
├── models/
│   ├── content_based.py
│   ├── collaborative_filtering.py
│   ├── hybrid.py
│   ├── popularity.py
│   ├── time_decay.py
│   ├── cold_start.py
│   ├── save_models.py
│   └── load_models.py
│
├── saved_models/
│
├── requirements.txt
├── README.md
└── .gitignore

Tech Stack
Python
FastAPI
Pandas
NumPy
Scikit-learn
TF-IDF
TruncatedSVD
Cosine Similarity

Installation
1️⃣ Create Virtual Environment
Windows
python -m venv RS_env
RS_env\Scripts\activate
Mac/Linux
python -m venv RS_env
source RS_env/bin/activate
2️⃣ Install Dependencies
pip install -r requirements.txt

Generate Synthetic Data
The system automatically generates datasets if they do not exist.
Generated files:
users.csv
brands.csv
reels.csv
interactions.csv

Run Retraining Pipeline
The retraining pipeline:
Loads datasets
Performs preprocessing
Builds recommendation models
Saves trained models
python -m src.pipeline.retrain
The retraining loop automatically updates the recommendation models periodically.

Run API Server
uvicorn src.api.main:app --reload

API Documentation:
http://127.0.0.1:8000/docs
API Endpoints
Recommend Reels
POST /recommend
Example Request
{
  "user_id": 9999,
  "k": 10
}
Example Response
{
  "user_id": 9999,
  "recommended_reels": [12, 55, 91, 201],
  "model": "hybrid"
}

Add User
POST /add_user

Add Reel
POST /add_reel

Add Interaction
POST /add_interaction

Add Brand
POST /add_brand

Automatic Retraining
The system supports automatic retraining using a background loop.
Example:
retrain_loop(interval=3600)
This retrains the recommendation system every hour.

Evaluation Metrics
The recommendation system is evaluated using:
Precision@K
Recall@K
NDCG@K

Evaluation is performed on:
Item Level
Category Level

Cold Start Handling
The system handles cold-start users using:

Level 1
Hybrid recommendations for existing users.
Level 2
Content-based recommendations using user interests.
Level 3
Popularity fallback for completely new users.

Production Features
✅ Hybrid Recommendation System
✅ Cold Start Support
✅ Automatic Retraining
✅ FastAPI Integration
✅ Dynamic User/Interaction Updates
✅ Scalable Architecture
✅ Production-Ready Structure

System Workflow
User Request
      ↓
FastAPI API
      ↓
Recommendation Router
      ↓
Hybrid / Cold Start / Popularity
      ↓
Top-K Recommended Reels

Running the Full System
Terminal 1 → API Server
uvicorn src.api.main:app --reload
Terminal 2 → Retraining Service
python -m src.pipeline.retrain

This separation ensures:
Faster API responses
Stable retraining
Production-ready deployment

Future Improvements
Real-time recommendations
Redis caching
Docker deployment
Airflow scheduling
Deep Learning recommendation models
A/B testing pipeline
User embedding models

License
This project is built for educational and research purposes as part of the Alluvo platform development.