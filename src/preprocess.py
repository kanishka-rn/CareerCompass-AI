import pandas as pd
import os

# ==============================
# CAREERCOMPASS AI
# DATA PREPROCESSING
# ==============================

RAW_DATA_PATH = "data/raw/career_dataset.csv"
PROCESSED_DATA_PATH = "data/processed/career_processed.csv"


def clean_text(text):
    """
    Clean and normalize text data.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower().strip()

    # Replace semicolons with commas
    text = text.replace(";", ",")

    # Remove duplicate spaces
    text = " ".join(text.split())

    return text


def main():

    print("\n===== LOADING DATASET =====")

    # Load raw dataset
    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Original shape: {df.shape}")

    print("\n===== ORIGINAL COLUMNS =====")

    for column in df.columns:
        print(column)

    # ==============================
    # REMOVE DUPLICATES
    # ==============================

    original_rows = len(df)

    df = df.drop_duplicates()

    removed_rows = original_rows - len(df)

    print(f"\nDuplicate records removed: {removed_rows}")

    # ==============================
    # HANDLE MISSING VALUES
    # ==============================

    df = df.fillna("")

    # ==============================
    # CLEAN TEXT COLUMNS
    # ==============================

    text_columns = [
        "Education",
        "Skills",
        "Interests",
        "Recommended_Career"
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # ==============================
    # CLEAN CAREER DOMAIN
    # IMPORTANT:
    # DO NOT MAP DOMAINS TO "OTHER"
    # ==============================

    df["Career_Domain"] = (
        df["Career_Domain"]
        .astype(str)
        .str.strip()
    )

    # ==============================
    # CLEAN AGE
    # ==============================

    df["Age"] = pd.to_numeric(
        df["Age"],
        errors="coerce"
    )

    # Replace invalid age values with median
    if df["Age"].isna().sum() > 0:

        median_age = int(df["Age"].median())

        df["Age"] = df["Age"].fillna(
            median_age
        )

    df["Age"] = df["Age"].astype(int)

    # ==============================
    # REMOVE EMPTY DOMAINS
    # ==============================

    df = df[
        df["Career_Domain"].str.strip() != ""
    ]

    # ==============================
    # DISPLAY DISTRIBUTION
    # ==============================

    print("\n===== CAREER DOMAIN DISTRIBUTION =====\n")

    print(
        df["Career_Domain"]
        .value_counts()
    )

    print(
        f"\nTotal Career Domains: "
        f"{df['Career_Domain'].nunique()}"
    )

    # ==============================
    # CREATE OUTPUT DIRECTORY
    # ==============================

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    # ==============================
    # SAVE PROCESSED DATASET
    # ==============================

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        "\nProcessed dataset saved successfully!"
    )

    print(
        f"Final shape: {df.shape}"
    )

    print(
        f"\nSaved at:\n{PROCESSED_DATA_PATH}"
    )


if __name__ == "__main__":
    main()