import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hybrid_engine import load_model, recommendation_strength, recommend_career
from interest_normalizer import normalize_interests
from skill_normalizer import normalize_skills

MODEL = load_model()

def test_skill_aliases_case_and_duplicates():
    assert normalize_skills("DSA, data structures, PYTHON, BurpSuite, python") == ["data structures and algorithms", "python", "burp suite"]

def test_interest_aliases_are_centralized():
    assert normalize_interests("Data Analytics, Defensive Security, Cloud") == ["data analysis", "cybersecurity", "cloud computing"]

def test_realistic_profiles_choose_expected_domains():
    profiles = [
        ("B.Tech CSE", "Python, SQL, Power BI, Excel", "Data Science, Data Analytics", "Data & Analytics"),
        ("B.Tech CSE", "Python, TensorFlow, Deep Learning, Computer Vision", "Artificial Intelligence", "AI & Machine Learning"),
        ("B.Tech", "Networking, Linux, Burp Suite, Python", "Defensive Security, Ethical Hacking", "Cybersecurity"),
        ("B.Tech", "Linux, Docker, AWS, Kubernetes", "Cloud Computing, DevOps", "Cloud & DevOps"),
        ("B.Tech ECE", "Arduino, IoT, Microcontrollers, Embedded Systems", "Embedded Systems, Electronics", "Electronics Engineering"),
        ("Civil Engineering", "AutoCAD, Structural Analysis, Construction", "Civil Engineering, Infrastructure", "Civil Engineering"),
    ]
    for education, skills, interests, expected in profiles:
        assert recommend_career(18, education, skills, interests, model=MODEL)["career_domain"] == expected

def test_weak_and_ambiguous_profiles_expose_new_metadata():
    result = recommend_career(18, "B.Tech CSE", "Python", "Technology", model=MODEL)
    assert result["recommendation_strength"] == recommendation_strength(result["hybrid_score"])
    assert isinstance(result["close_alternatives"], list)
    assert "matched_strong_skills" in result and "matched_supporting_skills" in result
