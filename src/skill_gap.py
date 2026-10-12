"""Alias-aware skill gap analysis and personalized learning roadmaps."""
from career_knowledge import CAREER_ROADMAPS, CAREER_SKILLS
from skill_normalizer import normalize_skills

def analyze_skill_gap(user_skills, career_domain):
    known = set(normalize_skills(user_skills)); required = CAREER_SKILLS.get(career_domain, [])
    matched = [skill for skill in required if skill in known]; missing = [skill for skill in required if skill not in known]
    return {"matched_skills": matched, "missing_skills": missing, "recommended_skills": missing[:5], "skill_match": round(100 * len(matched) / len(required), 2) if required else 0.0}

def personalized_roadmap(user_skills, career_domain):
    known = set(normalize_skills(user_skills)); steps = []
    if career_domain == "AI & Machine Learning" and "python" in known: steps.append("Strengthen Python for data analysis with NumPy and Pandas")
    if career_domain == "Data & Analytics" and "sql" in known: steps.append("Apply SQL to increasingly complex analytics questions")
    if career_domain == "AI & Machine Learning" and "machine learning" in known: steps.append("Advance to deep learning, model deployment, and MLOps")
    return (steps + [step for step in CAREER_ROADMAPS.get(career_domain, []) if step not in steps])[:8]
