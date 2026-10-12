# CareerCompass AI

CareerCompass AI is a Python ML career recommendation system for students. It combines Logistic Regression with transparent skill, interest, education, and keyword matching to return three career domains, explain the primary match, identify skill gaps, and generate an adaptive roadmap.

## Features

- Canonical aliases: `ML`, `JS`, `DSA`, and `PowerBI` normalize consistently.
- Model-compatible inputs: `Profile_Text`, `Education`, and `Age`.
- Weighted, bounded hybrid scores and separate ML confidence.
- Skill gaps, adaptive 6–8 step roadmaps, JSON/CSV exports, and metadata.

## Run

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python src\train_model.py
python src\recommender.py
```

Example: skills `python, JS, DSA, ML, SQL, PowerBI`; interests `AI, Data Science`.

## Test

```powershell
python -m pytest -q
```

Exports are saved under `results/`. The pre-existing optional dashboard requires a separate Streamlit installation: `streamlit run app.py`.

## Limitations

Accuracy depends on the synthetic training dataset. Real outcome data, calibration, and fairness evaluation are needed before consequential use.
