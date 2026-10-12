"""Train, evaluate, and save the CareerCompass scikit-learn pipeline."""
from pathlib import Path
from datetime import date
import json, platform
import joblib, pandas as pd, sklearn
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT=Path(__file__).resolve().parents[1]; DATA_PATH=ROOT/"data"/"processed"/"career_processed.csv"; MODEL_PATH=ROOT/"models"/"career_compass_model.pkl"; METADATA_PATH=ROOT/"models"/"model_metadata.json"
REQUIRED={"Age","Education","Skills","Interests","Career_Domain"}
def train_model():
    if not DATA_PATH.exists(): raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")
    df=pd.read_csv(DATA_PATH); missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Dataset missing required columns: {', '.join(sorted(missing))}")
    df=df.dropna(subset=["Career_Domain"]).copy(); df["Skills"]=df["Skills"].fillna("").astype(str); df["Interests"]=df["Interests"].fillna("").astype(str); df["Education"]=df["Education"].fillna("Unknown").astype(str); df["Age"]=pd.to_numeric(df["Age"],errors="coerce").fillna(df["Age"].median())
    df["Profile_Text"]=(df["Skills"]+" "+df["Interests"]).str.lower().str.strip(); X=df[["Profile_Text","Education","Age"]]; y=df["Career_Domain"]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    preprocessor=ColumnTransformer([("profile",TfidfVectorizer(stop_words="english",ngram_range=(1,2)),"Profile_Text"),("education",OneHotEncoder(handle_unknown="ignore"),["Education"]),("age","passthrough",["Age"])])
    model=Pipeline([("preprocessor",preprocessor),("classifier",LogisticRegression(max_iter=3000,random_state=42))]); model.fit(X_train,y_train); predictions=model.predict(X_test); accuracy=float(accuracy_score(y_test,predictions))
    print(f"Dataset size: {len(df)}\nAccuracy: {accuracy:.4f}\n\nClassification report:\n{classification_report(y_test,predictions,zero_division=0)}")
    MODEL_PATH.parent.mkdir(exist_ok=True); joblib.dump(model,MODEL_PATH)
    metadata={"model_name":"LogisticRegression with TF-IDF and ColumnTransformer","training_date":date.today().isoformat(),"dataset_size":len(df),"accuracy":accuracy,"features_used":["Profile_Text","Education","Age"],"career_domains":sorted(y.unique().tolist()),"python_version":platform.python_version(),"scikit_learn_version":sklearn.__version__}; METADATA_PATH.write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    print(f"\nSaved model: {MODEL_PATH}\nSaved metadata: {METADATA_PATH}"); return model,metadata
if __name__=="__main__": train_model()
