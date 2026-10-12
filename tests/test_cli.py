import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cli import CareerCompassCLI

def test_valid_profile_creation():
    app = CareerCompassCLI()
    profile = app.set_profile("18", "B.Tech CSE", "Python, ML", "AI")
    assert profile.age == 18 and profile.skills == ["python", "machine learning"]

@pytest.mark.parametrize("age", ["not-a-number", "14", "101"])
def test_invalid_age_handling(age):
    with pytest.raises(ValueError): CareerCompassCLI().set_profile(age, "B.Tech", "Python", "AI")

@pytest.mark.parametrize("skills, interests", [("", "AI"), ("Python", "")])
def test_empty_skill_or_interest_handling(skills, interests):
    with pytest.raises(ValueError): CareerCompassCLI().set_profile("18", "B.Tech", skills, interests)

def test_export_career_report(tmp_path):
    app = CareerCompassCLI(); app.set_profile("18", "B.Tech CSE", "Python, ML", "AI")
    app.result = {"career_domain":"AI & Machine Learning", "hybrid_score":80.0, "ml_score":85.0, "skill_score":50.0, "interest_score":100.0, "education_score":100.0, "career_roles":["AI Engineer"], "matched_skills":["python"], "missing_skills":["statistics"], "recommended_skills":["statistics"]}
    report = app.export_report(tmp_path)
    with report.open(encoding="utf-8") as handle: row = next(csv.DictReader(handle))
    assert report.exists() and row["Recommended Career"] == "AI & Machine Learning"

def test_resetting_current_profile():
    app = CareerCompassCLI(); app.set_profile("18", "B.Tech", "Python", "AI"); app.result = {"career_domain":"AI & Machine Learning"}
    app.reset_profile()
    assert app.profile is None and app.result is None
