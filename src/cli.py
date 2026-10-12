"""Professional interactive command-line interface for CareerCompass AI."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hybrid_engine import load_model, recommend_career
from recommender import validate_profile

EXPORTS_DIR = Path(__file__).resolve().parents[1] / "exports"
DIVIDER = "=" * 64

@dataclass
class Profile:
    age: int
    education: str
    skills: list[str]
    interests: str

class CareerCompassCLI:
    """Stores the current profile/result and handles the menu-driven application."""
    def __init__(self, model=None):
        self.model = model
        self.profile: Profile | None = None
        self.result: dict | None = None

    def set_profile(self, age, education, skills, interests):
        """Validate and store one profile; clears any previous result."""
        age, education, skills, interests = validate_profile(age, education, skills, interests)
        self.profile = Profile(age, education, skills, interests)
        self.result = None
        return self.profile

    def reset_profile(self):
        """Clear the active profile and recommendation for another user."""
        self.profile = None
        self.result = None

    def analyze_current_profile(self):
        if self.profile is None:
            raise ValueError("Please enter a profile first.")
        model = self.model or load_model()
        self.result = recommend_career(self.profile.age, self.profile.education, self.profile.skills, self.profile.interests, model=model)
        return self.result

    def export_report(self, export_directory=EXPORTS_DIR):
        """Export the current complete report using only Python's csv module."""
        if self.profile is None or self.result is None:
            raise ValueError("Please generate a career recommendation first.")
        directory = Path(export_directory); directory.mkdir(parents=True, exist_ok=True)
        filename = directory / f"career_report_{datetime.now():%Y%m%d_%H%M%S}.csv"
        fields = ["Age", "Education", "Skills", "Interests", "Recommended Career", "Hybrid Score", "ML Score", "Skill Match", "Interest Match", "Education Match", "Suggested Roles", "Matched Skills", "Missing Skills", "Recommended Skills"]
        row = {"Age": self.profile.age, "Education": self.profile.education, "Skills": ", ".join(self.profile.skills), "Interests": self.profile.interests, "Recommended Career": self.result["career_domain"], "Hybrid Score": self.result["hybrid_score"], "ML Score": self.result["ml_score"], "Skill Match": self.result["skill_score"], "Interest Match": self.result["interest_score"], "Education Match": self.result["education_score"], "Suggested Roles": ", ".join(self.result["career_roles"]), "Matched Skills": ", ".join(self.result["matched_skills"]), "Missing Skills": ", ".join(self.result["missing_skills"]), "Recommended Skills": ", ".join(self.result["recommended_skills"])}
        with filename.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerow(row)
        return filename

    def prompt_for_profile(self):
        """Keep asking until a valid profile is supplied or input is interrupted."""
        print("\nUSER PROFILE")
        while True:
            try:
                self.set_profile(input("Enter your age: "), input("Enter your education: "), input("Enter your skills (comma separated): "), input("Enter your interests (comma separated): "))
                print("Profile saved successfully.")
                return
            except ValueError as error:
                print(f"Invalid profile: {error} Please try again.\n")

    @staticmethod
    def _print_breakdown(item):
        print(f"Hybrid Score: {item['hybrid_score']:.2f}%\nML Prediction: {item['ml_score']:.2f}%\nSkill Match: {item['skill_score']:.2f}%\nInterest Match: {item['interest_score']:.2f}%\nEducation Match: {item['education_score']:.2f}%")
        print("Matched Skills: " + (", ".join(item["matched_skills"]) or "No direct matches yet"))

    def show_recommendation(self):
        result = self.analyze_current_profile(); print(f"\n{DIVIDER}\nCAREER RECOMMENDATION\n{DIVIDER}\n\nRecommended Career Domain: {result['career_domain']}")
        self._print_breakdown(result); print("\nWhy This Career?")
        for reason in result["why"]: print(f"- {reason}")
        print("\nSuggested Roles:")
        for role in result["career_roles"]: print(f"- {role}")

    def show_top_matches(self):
        result = self.analyze_current_profile(); print(f"\n{DIVIDER}\nTOP 3 CAREER MATCHES\n{DIVIDER}")
        for rank, item in enumerate(result["top_results"], 1):
            print(f"\n{rank}. {item['career_domain']}"); self._print_breakdown(item)
            print("Why This Career?: " + "; ".join(result["why"] if rank == 1 else [f"Hybrid evidence score: {item['hybrid_score']:.2f}%"]))

    def show_skill_gap(self):
        result = self.analyze_current_profile(); print(f"\n{DIVIDER}\nSKILL GAP ANALYSIS\n{DIVIDER}\nCareer Domain: {result['career_domain']}\nOverall Skill Match: {result['skill_match']:.1f}%")
        print("\nSkills You Already Have:"); print("\n".join(f"- {skill}" for skill in result["matched_skills"]) or "- No direct skill matches found yet.")
        print("\nSkills To Improve:"); print("\n".join(f"- {skill}" for skill in result["missing_skills"]) or "- Excellent! No major missing skills.")
        print("\nRecommended Skills To Learn:"); print("\n".join(f"{index}. {skill}" for index, skill in enumerate(result["recommended_skills"], 1)) or "Continue building advanced projects.")

    def show_roadmap(self):
        if self.result is None: raise ValueError("Please generate a career recommendation first.")
        print(f"\n{DIVIDER}\nPERSONALIZED CAREER ROADMAP\n{DIVIDER}\nRecommended Career: {self.result['career_domain']}")
        for index, step in enumerate(self.result["roadmap"], 1): print(f"\nSTEP {index}\n{step}")

def print_menu():
    print(f"\nCAREERCOMPASS AI\n{DIVIDER}\nAI-Powered Career Recommendation System\n{DIVIDER}\n1. Get Career Recommendation\n2. View Top 3 Career Matches\n3. Analyze Skill Gap\n4. View Personalized Career Roadmap\n5. Export Career Report\n6. Try Another Profile\n7. Exit")

def main():
    app = CareerCompassCLI()
    print("CAREERCOMPASS AI\n" + DIVIDER + "\nAI-Powered Career Recommendation System\n" + DIVIDER)
    try:
        app.prompt_for_profile()
        while True:
            print_menu(); choice = input("Enter your choice: ").strip()
            try:
                if choice == "1": app.show_recommendation()
                elif choice == "2": app.show_top_matches()
                elif choice == "3": app.show_skill_gap()
                elif choice == "4": app.show_roadmap()
                elif choice == "5": print(f"Career report exported successfully!\nFile: {app.export_report()}")
                elif choice == "6": app.reset_profile(); app.prompt_for_profile()
                elif choice == "7": print(f"\n{DIVIDER}\nThank you for using CareerCompass AI!\nKeep learning, keep building, and find your path!\n{DIVIDER}"); return
                else: print("Invalid menu choice. Please enter a number from 1 to 7.")
            except (ValueError, FileNotFoundError, OSError) as error: print(f"Unable to complete that action: {error}")
    except (EOFError, KeyboardInterrupt): print("\nSession ended safely.")

if __name__ == "__main__": main()
