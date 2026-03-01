import pandas as pd
import ast

# تحميل الملفات
users_df = pd.read_csv("data/raw/users.csv")
brands_df = pd.read_csv("data/raw/brands.csv")
reels_df = pd.read_csv("data/raw/reels.csv")
interactions_df = pd.read_csv("data/raw/interactions.csv")

# تحويل الأعمدة اللي فيها lists
users_df['interests'] = users_df['interests'].apply(ast.literal_eval)
users_df['followed_brands'] = users_df['followed_brands'].apply(ast.literal_eval)

# تحويل التواريخ
users_df['created_at'] = pd.to_datetime(users_df['created_at'])
reels_df['created_at'] = pd.to_datetime(reels_df['created_at'])
interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])

# تجربة سريعة
print(users_df.head())
print(brands_df.head())
print(reels_df.head())
print(interactions_df.head())