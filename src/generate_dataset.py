import pandas as pd
import random
from faker import Faker

fake = Faker()

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

NUM_SAMPLES_PER_CAREER = 40

career_data = {

    # ==================================================
    # SOFTWARE & TECHNOLOGY
    # ==================================================

    "Software Development": {
        "education": [
            "B.Tech Computer Science",
            "B.Tech Information Technology",
            "B.Sc Computer Science",
            "MCA"
        ],
        "skills": [
            "python", "java", "c++", "c programming",
            "data structures", "algorithms",
            "html", "css", "javascript",
            "git", "sql"
        ],
        "interests": [
            "software development",
            "web development",
            "application development",
            "programming"
        ],
        "careers": [
            "Software Developer",
            "Software Engineer",
            "Backend Developer",
            "Frontend Developer",
            "Full Stack Developer"
        ]
    },

    "AI & Machine Learning": {
        "education": [
            "B.Tech Artificial Intelligence",
            "B.Tech Computer Science",
            "B.Sc Data Science",
            "B.Sc Computer Science",
            "M.Sc Artificial Intelligence"
        ],
        "skills": [
            "python",
            "machine learning",
            "deep learning",
            "data analysis",
            "statistics",
            "numpy",
            "pandas",
            "tensorflow",
            "pytorch"
        ],
        "interests": [
            "artificial intelligence",
            "machine learning",
            "generative ai",
            "computer vision",
            "data science"
        ],
        "careers": [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist",
            "Deep Learning Engineer",
            "Computer Vision Engineer"
        ]
    },

    "Data & Analytics": {
        "education": [
            "B.Tech Data Science",
            "B.Sc Data Science",
            "B.Sc Mathematics",
            "B.Com",
            "BBA",
            "Economics"
        ],
        "skills": [
            "python",
            "sql",
            "excel",
            "power bi",
            "statistics",
            "data visualization",
            "pandas"
        ],
        "interests": [
            "data analysis",
            "business analytics",
            "statistics",
            "data visualization"
        ],
        "careers": [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "Business Intelligence Analyst"
        ]
    },

    "Cloud & DevOps": {
        "education": [
            "B.Tech Computer Science",
            "B.Tech Information Technology",
            "B.Tech ECE"
        ],
        "skills": [
            "linux",
            "docker",
            "aws",
            "azure",
            "kubernetes",
            "python",
            "git"
        ],
        "interests": [
            "cloud computing",
            "devops",
            "system administration"
        ],
        "careers": [
            "Cloud Engineer",
            "DevOps Engineer",
            "Site Reliability Engineer"
        ]
    },

    "Cybersecurity": {
        "education": [
            "B.Tech Computer Science",
            "B.Tech Information Technology",
            "B.Sc Cybersecurity"
        ],
        "skills": [
            "networking",
            "linux",
            "python",
            "cybersecurity",
            "ethical hacking",
            "network security"
        ],
        "interests": [
            "cybersecurity",
            "ethical hacking",
            "network security"
        ],
        "careers": [
            "Cybersecurity Analyst",
            "Security Engineer",
            "Penetration Tester"
        ]
    },

    # ==================================================
    # CORE ENGINEERING
    # ==================================================

    "Mechanical Engineering": {
        "education": [
            "B.Tech Mechanical Engineering",
            "B.E Mechanical Engineering"
        ],
        "skills": [
            "autocad",
            "solidworks",
            "thermodynamics",
            "manufacturing",
            "mechanical design"
        ],
        "interests": [
            "automobile",
            "manufacturing",
            "robotics",
            "mechanical design"
        ],
        "careers": [
            "Mechanical Engineer",
            "Design Engineer",
            "Automotive Engineer",
            "Manufacturing Engineer"
        ]
    },

    "Civil Engineering": {
        "education": [
            "B.Tech Civil Engineering",
            "B.E Civil Engineering"
        ],
        "skills": [
            "autocad",
            "structural analysis",
            "construction management",
            "surveying",
            "revit"
        ],
        "interests": [
            "construction",
            "infrastructure",
            "structural engineering"
        ],
        "careers": [
            "Civil Engineer",
            "Structural Engineer",
            "Site Engineer",
            "Construction Manager"
        ]
    },

    "Electronics Engineering": {
        "education": [
            "B.Tech ECE",
            "B.E Electronics and Communication Engineering"
        ],
        "skills": [
            "embedded systems",
            "iot",
            "arduino",
            "electronics",
            "microcontrollers",
            "communication systems"
        ],
        "interests": [
            "electronics",
            "embedded systems",
            "iot",
            "robotics"
        ],
        "careers": [
            "Embedded Systems Engineer",
            "IoT Engineer",
            "Electronics Engineer"
        ]
    },

    "Electrical Engineering": {
        "education": [
            "B.Tech EEE",
            "B.E Electrical Engineering"
        ],
        "skills": [
            "power systems",
            "electrical circuits",
            "matlab",
            "control systems",
            "embedded systems"
        ],
        "interests": [
            "power systems",
            "renewable energy",
            "automation"
        ],
        "careers": [
            "Electrical Engineer",
            "Power Systems Engineer",
            "Automation Engineer"
        ]
    },

    # ==================================================
    # COMMERCE & BUSINESS
    # ==================================================

    "Finance & Accounting": {
        "education": [
            "B.Com",
            "B.Com Accounting and Finance",
            "BBA Finance",
            "MBA Finance"
        ],
        "skills": [
            "accounting",
            "financial analysis",
            "excel",
            "taxation",
            "financial reporting"
        ],
        "interests": [
            "finance",
            "banking",
            "investment",
            "accounting"
        ],
        "careers": [
            "Financial Analyst",
            "Accountant",
            "Investment Analyst",
            "Finance Manager"
        ]
    },

    "Business & Management": {
        "education": [
            "BBA",
            "B.Com",
            "MBA",
            "B.Tech"
        ],
        "skills": [
            "communication",
            "leadership",
            "project management",
            "business analysis",
            "excel"
        ],
        "interests": [
            "management",
            "entrepreneurship",
            "business",
            "strategy"
        ],
        "careers": [
            "Business Analyst",
            "Project Manager",
            "Operations Manager",
            "Management Consultant"
        ]
    },

    "Marketing": {
        "education": [
            "BBA",
            "B.Com",
            "BA Marketing",
            "MBA Marketing"
        ],
        "skills": [
            "digital marketing",
            "seo",
            "social media",
            "content marketing",
            "communication"
        ],
        "interests": [
            "marketing",
            "branding",
            "social media",
            "advertising"
        ],
        "careers": [
            "Digital Marketing Specialist",
            "Marketing Manager",
            "SEO Specialist",
            "Brand Manager"
        ]
    },

    # ==================================================
    # MEDICAL & HEALTHCARE
    # ==================================================

    "Medicine": {
        "education": [
            "MBBS",
            "MD",
            "Medical Student"
        ],
        "skills": [
            "medical diagnosis",
            "patient care",
            "clinical research",
            "biology"
        ],
        "interests": [
            "medicine",
            "healthcare",
            "patient care",
            "medical research"
        ],
        "careers": [
            "Doctor",
            "Medical Researcher",
            "Clinical Specialist"
        ]
    },

    "Pharmacy": {
        "education": [
            "B.Pharm",
            "M.Pharm"
        ],
        "skills": [
            "pharmacology",
            "drug research",
            "clinical research",
            "chemistry"
        ],
        "interests": [
            "pharmaceutical research",
            "drug development",
            "healthcare"
        ],
        "careers": [
            "Pharmacist",
            "Clinical Research Associate",
            "Drug Safety Specialist"
        ]
    },

    "Healthcare": {
        "education": [
            "B.Sc Nursing",
            "BPT",
            "Medical Laboratory Science"
        ],
        "skills": [
            "patient care",
            "medical knowledge",
            "communication",
            "clinical procedures"
        ],
        "interests": [
            "healthcare",
            "patient care",
            "medicine"
        ],
        "careers": [
            "Nurse",
            "Physiotherapist",
            "Medical Laboratory Technologist"
        ]
    },

    # ==================================================
    # SCIENCE & RESEARCH
    # ==================================================

    "Scientific Research": {
        "education": [
            "B.Sc Physics",
            "B.Sc Chemistry",
            "B.Sc Mathematics",
            "M.Sc",
            "PhD"
        ],
        "skills": [
            "research",
            "statistics",
            "data analysis",
            "scientific writing",
            "experimentation"
        ],
        "interests": [
            "research",
            "science",
            "experimentation",
            "academia"
        ],
        "careers": [
            "Research Scientist",
            "Research Analyst",
            "Scientist",
            "Academic Researcher"
        ]
    },

    # ==================================================
    # DESIGN
    # ==================================================

    "UI/UX & Design": {
        "education": [
            "B.Des",
            "B.Sc Design",
            "B.Tech",
            "BA Design"
        ],
        "skills": [
            "figma",
            "ui design",
            "ux research",
            "prototyping",
            "adobe xd"
        ],
        "interests": [
            "design",
            "user experience",
            "creativity",
            "product design"
        ],
        "careers": [
            "UI Designer",
            "UX Designer",
            "Product Designer",
            "UX Researcher"
        ]
    }
}


# --------------------------------------------------
# DATASET GENERATION
# --------------------------------------------------

rows = []
candidate_id = 1

for domain, details in career_data.items():

    for _ in range(NUM_SAMPLES_PER_CAREER):

        education = random.choice(details["education"])

        selected_skills = random.sample(
            details["skills"],
            k=random.randint(
                max(2, len(details["skills"]) // 2),
                len(details["skills"])
            )
        )

        selected_interests = random.sample(
            details["interests"],
            k=random.randint(1, len(details["interests"]))
        )

        career = random.choice(details["careers"])

        score = round(random.uniform(0.80, 0.98), 2)

        rows.append({
            "CandidateID": candidate_id,
            "Age": random.randint(18, 35),
            "Education": education,
            "Skills": ";".join(selected_skills),
            "Interests": ";".join(selected_interests),
            "Career_Domain": domain,
            "Recommended_Career": career,
            "Recommendation_Score": score
        })

        candidate_id += 1


# --------------------------------------------------
# SAVE DATASET
# --------------------------------------------------

df = pd.DataFrame(rows)

output_path = "data/raw/career_dataset.csv"

df.to_csv(output_path, index=False)

print("\n========================================")
print("CAREER DATASET GENERATED SUCCESSFULLY")
print("========================================")

print(f"\nTotal Records: {len(df)}")

print("\nCareer Domain Distribution:\n")

print(df["Career_Domain"].value_counts())

print(f"\nDataset saved at: {output_path}")
