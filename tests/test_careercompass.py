import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from skill_normalizer import normalize_skills
from skill_gap import analyze_skill_gap
from recommender import validate_profile
from hybrid_engine import calculate_hybrid_scores

def test_alias_normalization_and_deduplication():
    assert normalize_skills("ML, machine learning, JS, DSA, PowerBI") == ["machine learning","javascript","data structures and algorithms","power bi"]
def test_alias_matches_canonical_requirement():
    analysis=analyze_skill_gap("ML, Python", "AI & Machine Learning")
    assert "machine learning" in analysis["matched_skills"] and "machine learning" not in analysis["missing_skills"]
def test_input_validation():
    assert validate_profile("18","B.Tech CSE","JS, JS, ML","AI") == (18,"B.Tech CSE",["javascript","machine learning"],"AI")
def test_hybrid_scores_are_bounded_and_ranked():
    class Model:
        classes_=["AI & Machine Learning","Data & Analytics"]
        def predict_proba(self, frame): return [[.7,.3]]
    scores=calculate_hybrid_scores(Model(),18,"B.Tech CSE","Python, ML, SQL","AI, Data Science")
    assert all(0<=item["hybrid_score"]<=100 for item in scores)
    assert scores==sorted(scores,key=lambda item:item["hybrid_score"],reverse=True)
