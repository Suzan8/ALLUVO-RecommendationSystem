from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()

user_interests = pd.DataFrame(
    mlb.fit_transform(users_df['interests']),
    columns=[f"interest_{c}" for c in mlb.classes_],
    index=users_df.index
)
users_df = pd.concat([users_df, user_interests], axis=1)