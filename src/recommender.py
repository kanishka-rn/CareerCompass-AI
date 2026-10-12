"""CareerCompass command-line application."""
from pathlib import Path
from datetime import datetime
import csv, json
from hybrid_engine import recommend_career, score_rating
from skill_normalizer import normalize_skills

def validate_profile(age, education, skills, interests):
    try: age=int(age)
    except (TypeError,ValueError): raise ValueError("Age must be a whole number.")
    if not 15<=age<=100: raise ValueError("Age must be between 15 and 100.")
    if not str(education).strip(): raise ValueError("Education cannot be empty.")
    normalized=normalize_skills(skills)
    if not normalized: raise ValueError("Enter at least one skill.")
    if not str(interests).strip(): raise ValueError("Interests cannot be empty.")
    return age,str(education).strip(),normalized,str(interests).strip()

def export_result(result, choice):
    directory=Path(__file__).resolve().parents[1]/"results"; directory.mkdir(exist_ok=True); stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); outputs=[]
    if choice in ("1","3"):
        path=directory/f"career_result_{stamp}.json"; path.write_text(json.dumps(result,indent=2),encoding="utf-8"); outputs.append(path)
    if choice in ("2","3"):
        path=directory/f"career_result_{stamp}.csv"; fields=["rank","career_domain","hybrid_score","rating","ml_score","skill_score","interest_score","education_score","keyword_score"]
        with path.open("w",newline="",encoding="utf-8") as handle:
            writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader()
            for rank,item in enumerate(result["top_results"],1): writer.writerow({"rank":rank,"rating":score_rating(item["hybrid_score"]),**{field:item.get(field,"") for field in fields if field not in {"rank","rating"}}})
        outputs.append(path)
    return outputs

def display_results(result,age,education):
    print("\n"+"="*65+"\nCAREERCOMPASS AI | Intelligent Career Recommendation\n"+"="*65)
    print(f"\nPROFILE SUMMARY\nAge: {age}\nEducation: {education}\nNormalized Skills: {', '.join(result['normalized_skills'])}")
    print("\nTOP CAREER MATCHES")
    for rank,item in enumerate(result["top_results"],1): print(f"{rank}. {item['career_domain']} | Hybrid Match: {item['hybrid_score']:.1f}% ({score_rating(item['hybrid_score'])}) | ML Confidence: {item['ml_score']:.1f}%")
    print(f"\nPRIMARY RECOMMENDATION: {result['career_domain']} — {result['confidence']:.1f}% ({result['rating']})")
    print("\nWHY THIS CAREER?\n"+"\n".join(f"- {reason}." for reason in result["why"]))
    print("\nSKILL GAP ANALYSIS\nAlready have: "+(", ".join(result["matched_skills"]) or "No direct core matches yet")+"\nTo improve: "+(", ".join(result["missing_skills"]) or "No major gaps"))
    print("\nNEXT BEST SKILLS\n"+"\n".join(f"{i}. {skill}" for i,skill in enumerate(result["recommended_skills"],1)))
    print("\nPERSONALIZED ROADMAP\n"+"\n".join(f"{i}. {step}" for i,step in enumerate(result["roadmap"],1)))
    print("\nCAREER ROLES\n"+", ".join(result["career_roles"]))

def main():
    try:
        age,education,skills,interests=validate_profile(input("Age: "),input("Education: "),input("Skills (comma-separated): "),input("Interests: "))
        result=recommend_career(age,education,skills,interests); display_results(result,age,education)
        choice=input("\nSave this result? 1. JSON  2. CSV  3. Both  4. No: ").strip()
        if choice in {"1","2","3"}: print("Saved: "+", ".join(map(str,export_result(result,choice))))
    except (ValueError,FileNotFoundError) as error: print(f"\nError: {error}")
if __name__=="__main__": main()
