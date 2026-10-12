import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score, f1_score


INPUT_PATH = "data/processed/career_processed.csv"


def load_and_prepare_data():

    df = pd.read_csv(INPUT_PATH)

    # Combine Skills and Interests
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

    X = df[
        [
            "Profile_Text",
            "Education",
            "Age"
        ]
    ]

    y = df["Career_Domain"]

    return X, y


def create_preprocessor():

    return ColumnTransformer(
        transformers=[
            (
                "text",
                TfidfVectorizer(
                    max_features=150,
                    ngram_range=(1, 2)
                ),
                "Profile_Text"
            ),
            (
                "education",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                ["Education"]
            ),
            (
                "age",
                StandardScaler(),
                ["Age"]
            )
        ]
    )


def main():

    print("\n===== LOADING DATA =====")

    X, y = load_and_prepare_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced"
        ),

        "Linear SVM": LinearSVC(
            class_weight="balanced",
            random_state=42
        )
    }

    results = []

    print("\n===== TRAINING MODELS =====")

    for name, classifier in models.items():

        print(f"\nTraining: {name}")

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    create_preprocessor()
                ),
                (
                    "classifier",
                    classifier
                )
            ]
        )

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        results.append(
            {
                "Model": name,
                "Accuracy": accuracy,
                "Weighted F1 Score": f1
            }
        )

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="Weighted F1 Score",
        ascending=False
    )

    print("\n===== MODEL COMPARISON =====")

    print(
        results_df.to_string(
            index=False
        )
    )

    best_model = results_df.iloc[0]

    print("\n===== BEST MODEL =====")

    print(
        f"Model: {best_model['Model']}"
    )

    print(
        f"Accuracy: {best_model['Accuracy']:.4f}"
    )

    print(
        f"Weighted F1 Score: "
        f"{best_model['Weighted F1 Score']:.4f}"
    )


if __name__ == "__main__":
    main()