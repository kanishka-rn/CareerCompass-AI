import pandas as pd


INPUT_PATH = "data/processed/career_processed.csv"


def load_data():
    return pd.read_csv(INPUT_PATH)


def create_profile_text(df):
    """
    Combine skills and interests into
    one text feature for NLP vectorization.
    """

    df["Profile_Text"] = (
        df["Skills"].fillna("")
        + " "
        + df["Interests"].fillna("")
    )

    df["Profile_Text"] = (
        df["Profile_Text"]
        .str.lower()
        .str.replace(";", " ", regex=False)
        .str.strip()
    )

    return df


def inspect_features(df):

    print("\n===== DATASET SHAPE =====")
    print(df.shape)

    print("\n===== ML INPUT FEATURES =====")
    print("""
1. Profile_Text
   → Skills + Interests

2. Education

3. Age
""")

    print("===== TARGET =====")
    print("Career_Domain")

    print("\n===== SAMPLE PROFILE TEXT =====")
    print(df["Profile_Text"].head())


def main():

    print("Loading processed dataset...")

    df = load_data()

    df = create_profile_text(df)

    inspect_features(df)


if __name__ == "__main__":
    main()