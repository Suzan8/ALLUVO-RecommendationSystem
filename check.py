import pandas as pd

df = pd.read_csv("data/raw/interactions.csv")
print("TOTAL:", len(df))

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%m/%d/%Y %I:%M:%S %p",
    errors="coerce"
)

print("VALID:", df["timestamp"].notna().sum())