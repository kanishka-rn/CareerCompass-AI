"""Domain evidence used for explanations and deterministic score tie-breaking."""
from career_knowledge import CAREER_SKILLS

DOMAIN_EVIDENCE = {
    "Software Development": {"strong_skills": ["javascript", "data structures and algorithms", "algorithms"], "supporting_skills": ["python", "java", "git"], "strong_interests": ["programming", "coding", "web development"], "supporting_interests": ["software development", "app development"]},
    "AI & Machine Learning": {"strong_skills": ["machine learning", "deep learning", "tensorflow", "pytorch", "computer vision"], "supporting_skills": ["python", "numpy", "pandas", "statistics"], "strong_interests": ["artificial intelligence", "machine learning", "deep learning"], "supporting_interests": ["data science", "computer vision"]},
    "Data & Analytics": {"strong_skills": ["sql", "power bi", "tableau", "data analysis"], "supporting_skills": ["python", "excel", "pandas", "statistics"], "strong_interests": ["data science", "data analysis", "analytics"], "supporting_interests": ["business intelligence", "visualization"]},
    "Cloud & DevOps": {"strong_skills": ["aws", "docker", "kubernetes", "ci/cd"], "supporting_skills": ["linux", "networking", "git", "python"], "strong_interests": ["cloud computing", "devops"], "supporting_interests": ["automation", "infrastructure"]},
    "Cybersecurity": {"strong_skills": ["burp suite", "wireshark", "ethical hacking", "penetration testing"], "supporting_skills": ["python", "linux", "networking", "cryptography"], "strong_interests": ["ethical hacking", "defensive security", "web security"], "supporting_interests": ["cybersecurity", "network security"]},
    "Mechanical Engineering": {"strong_skills": ["cad", "solidworks", "thermodynamics"], "supporting_skills": ["autocad", "manufacturing", "robotics"], "strong_interests": ["mechanical engineering", "machines"], "supporting_interests": ["robotics", "manufacturing"]},
    "Civil Engineering": {"strong_skills": ["autocad", "structural analysis", "construction"], "supporting_skills": ["surveying", "project management"], "strong_interests": ["civil engineering", "construction"], "supporting_interests": ["infrastructure", "structural design"]},
    "Electronics Engineering": {"strong_skills": ["embedded systems", "microcontrollers", "iot", "arduino"], "supporting_skills": ["electronics", "pcb design", "vlsi", "c programming"], "strong_interests": ["embedded systems", "electronics"], "supporting_interests": ["iot", "hardware"]},
    "Electrical Engineering": {"strong_skills": ["power systems", "control systems", "circuits"], "supporting_skills": ["automation", "matlab"], "strong_interests": ["electrical engineering", "power systems"], "supporting_interests": ["automation", "renewable energy"]},
}

for _domain, _skills in CAREER_SKILLS.items():
    DOMAIN_EVIDENCE.setdefault(_domain, {"strong_skills": _skills[:3], "supporting_skills": _skills[3:6], "strong_interests": [], "supporting_interests": []})

def evaluate_domain_evidence(domain, skills, interests):
    """Return matched strong/supporting evidence and a separate 0–100 evidence score."""
    data = DOMAIN_EVIDENCE[domain]; known_skills = set(skills); known_interests = set(interests)
    strong_skills = [item for item in data["strong_skills"] if item in known_skills]
    supporting_skills = [item for item in data["supporting_skills"] if item in known_skills]
    strong_interests = [item for item in data["strong_interests"] if item in known_interests]
    supporting_interests = [item for item in data["supporting_interests"] if item in known_interests]
    possible = len(data["strong_skills"])*3 + len(data["supporting_skills"]) + len(data["strong_interests"])*3 + len(data["supporting_interests"])
    earned = len(strong_skills)*3 + len(supporting_skills) + len(strong_interests)*3 + len(supporting_interests)
    return {"matched_strong_skills": strong_skills, "matched_supporting_skills": supporting_skills, "matched_strong_interests": strong_interests, "matched_supporting_interests": supporting_interests, "evidence_score": round(100*earned/possible, 2) if possible else 0.0}
