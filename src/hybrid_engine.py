"""Hybrid recommendations: fixed 40/30/20/10 score plus transparent evidence metadata."""
from __future__ import annotations
from pathlib import Path
import joblib
import pandas as pd
from career_knowledge import CAREER_INTERESTS, CAREER_ROLES, CAREER_SKILLS
from domain_evidence import evaluate_domain_evidence
from interest_normalizer import normalize_interests
from skill_gap import analyze_skill_gap, personalized_roadmap
from skill_normalizer import normalize_skills, normalize_text

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "career_compass_model.pkl"
WEIGHTS = {"ml": 0.40, "skill": 0.30, "interest": 0.20, "education": 0.10}
EDUCATION_KEYWORDS = {"AI & Machine Learning": ("computer", "cse", "information technology", "it", "math", "engineering"), "Data & Analytics": ("computer", "cse", "information technology", "it", "math", "statistics", "commerce", "engineering"), "Electronics Engineering": ("electronics", "ece", "electrical and electronics"), "Electrical Engineering": ("electrical", "eee"), "Mechanical Engineering": ("mechanical",), "Civil Engineering": ("civil",), "Medicine": ("medical", "mbbs"), "Pharmacy": ("pharm",)}

def load_model(model_path: Path = MODEL_PATH):
    if not model_path.exists(): raise FileNotFoundError(f"Model not found: {model_path}. Run: python src\\train_model.py")
    return joblib.load(model_path)

def create_profile_text(age, education, skills, interests):
    """Produce the existing model's Profile_Text feature using canonical input tokens."""
    return " ".join(("skills", *normalize_skills(skills), "interests", *normalize_interests(interests), "education", normalize_text(education), "age", str(age)))

def calculate_ml_scores(model, age, education, skills, interests):
    frame = pd.DataFrame([{"Profile_Text": create_profile_text(age, education, skills, interests), "Education": str(education).strip(), "Age": age}])
    return {domain: round(float(probability)*100, 2) for domain, probability in zip(model.classes_, model.predict_proba(frame)[0])}

def calculate_skill_match(skills, career_domain):
    known, required = set(normalize_skills(skills)), CAREER_SKILLS.get(career_domain, [])
    matched = [skill for skill in required if skill in known]
    return (round(100*len(matched)/len(required), 2) if required else 0.0), matched

def calculate_interest_match(interests, career_domain):
    values = normalize_interests(interests); targets = [normalize_text(value) for value in CAREER_INTERESTS.get(career_domain, [])]
    if not values or not targets: return 0.0
    matched = sum(any(value == target or value in target or target in value for target in targets) for value in values)
    return round(100*matched/len(values), 2)

def calculate_education_match(education, career_domain):
    text = normalize_text(education)
    if not text: return 0.0
    keywords = EDUCATION_KEYWORDS.get(career_domain)
    return 75.0 if keywords is None else (100.0 if any(keyword in text for keyword in keywords) else 45.0)

def calculate_hybrid_scores(model, age, education, skills, interests):
    """Score every domain with the invariant formula: .40 ML + .30 skill + .20 interest + .10 education."""
    canonical_skills, canonical_interests = normalize_skills(skills), normalize_interests(interests); ml_scores = calculate_ml_scores(model, age, education, canonical_skills, canonical_interests); results=[]
    for domain in CAREER_ROLES:
        skill_score, matched_skills = calculate_skill_match(canonical_skills, domain); interest_score = calculate_interest_match(canonical_interests, domain); education_score = calculate_education_match(education, domain); ml_score = ml_scores.get(domain, 0.0)
        hybrid_score = round(ml_score*WEIGHTS["ml"] + skill_score*WEIGHTS["skill"] + interest_score*WEIGHTS["interest"] + education_score*WEIGHTS["education"], 2)
        evidence = evaluate_domain_evidence(domain, canonical_skills, canonical_interests)
        results.append({"career_domain":domain, "hybrid_score":min(100.0,max(0.0,hybrid_score)), "ml_score":ml_score, "skill_score":skill_score, "interest_score":interest_score, "education_score":education_score, "matched_skills":matched_skills, **evidence})
    # Evidence never changes Hybrid Score; it resolves otherwise equal rounded scores deterministically.
    return sorted(results, key=lambda item: (item["hybrid_score"], item["evidence_score"]), reverse=True)

def get_top_careers(model, age, education, skills, interests, limit=3): return calculate_hybrid_scores(model, age, education, skills, interests)[:limit]

def recommendation_strength(score):
    if score <= 30: return "Exploratory"
    if score <= 50: return "Developing Match"
    if score <= 70: return "Strong Match"
    return "Excellent Match"

def score_rating(score): return recommendation_strength(score)

def generate_career_explanation(result, education):
    """Explain a recommendation from its recorded evidence instead of generic claims."""
    reasons=[]
    if result["matched_strong_skills"]: reasons.append("Your strong skills include " + ", ".join(result["matched_strong_skills"]) + ".")
    if result["matched_supporting_skills"]: reasons.append("Supporting skills such as " + ", ".join(result["matched_supporting_skills"]) + " strengthen this profile.")
    if result["matched_strong_interests"]: reasons.append("Your strong interests include " + ", ".join(result["matched_strong_interests"]) + ".")
    elif result["interest_score"]: reasons.append(f"Your interests have a {result['interest_score']:.0f}% match with this domain.")
    if result["education_score"] >= 75: reasons.append(f"Your {education} background is relevant.")
    if not reasons: reasons.append("This is an exploratory option based on your current profile.")
    reasons.append(f"ML confidence is {result['ml_score']:.1f}%; hybrid match score is {result['hybrid_score']:.1f}%.")
    return reasons

def recommend_career(age, education, skills, interests, model=None):
    all_results = calculate_hybrid_scores(model or load_model(), age, education, skills, interests); top_results = all_results[:3]; primary=top_results[0]; gap=analyze_skill_gap(skills, primary["career_domain"])
    close_alternatives=[item["career_domain"] for item in all_results[1:] if primary["hybrid_score"]-item["hybrid_score"] <= 5]
    return {**primary, "confidence":primary["hybrid_score"], "rating":recommendation_strength(primary["hybrid_score"]), "recommendation_strength":recommendation_strength(primary["hybrid_score"]), "close_alternatives":close_alternatives, "career_roles":CAREER_ROLES[primary["career_domain"]], **gap, "roadmap":personalized_roadmap(skills, primary["career_domain"]), "top_results":top_results, "why":generate_career_explanation(primary, education), "normalized_skills":normalize_skills(skills), "normalized_interests":normalize_interests(interests)}
