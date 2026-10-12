import pandas as pd

DATA_PATH = "data/raw/career_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("\n===== DATASET OVERVIEW =====")
print(df.head())

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
for column in df.columns:
    print("-", column)

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== EDUCATION DISTRIBUTION =====")
print(df["Education"].value_counts())

print("\n===== RECOMMENDED CAREER DISTRIBUTION =====")
print(df["Recommended_Career"].value_counts())

print("\n===== RECOMMENDATION SCORE =====")
print(df["Recommendation_Score"].describe())