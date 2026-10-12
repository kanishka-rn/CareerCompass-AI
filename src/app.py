"""Streamlit dashboard for CareerCompass AI using the existing hybrid engine."""
from __future__ import annotations

import csv
import io
import re

import pandas as pd
import streamlit as st

from hybrid_engine import load_model, recommend_career
from recommender import validate_profile

st.set_page_config(page_title="CareerCompass AI", page_icon="🧭", layout="wide")

@st.cache_resource
def get_model():
    """Load the scikit-learn pipeline once per Streamlit server process."""
    return load_model()

def initialise_state():
    """Set up durable per-session analysis state."""
    st.session_state.setdefault("profile", None)
    st.session_state.setdefault("analysis", None)

def report_csv(profile, result):
    """Create the requested single-row CSV report in memory."""
    fields = ["Age", "Education", "Skills", "Interests", "Recommended Career", "Hybrid Score", "ML Score", "Skill Match", "Interest Match", "Education Match", "Suggested Roles", "Matched Skills", "Missing Skills", "Recommended Skills"]
    row = {"Age": profile["age"], "Education": profile["education"], "Skills": ", ".join(profile["skills"]), "Interests": profile["interests"], "Recommended Career": result["career_domain"], "Hybrid Score": result["hybrid_score"], "ML Score": result["ml_score"], "Skill Match": result["skill_score"], "Interest Match": result["interest_score"], "Education Match": result["education_score"], "Suggested Roles": ", ".join(result["career_roles"]), "Matched Skills": ", ".join(result["matched_skills"]), "Missing Skills": ", ".join(result["missing_skills"]), "Recommended Skills": ", ".join(result["recommended_skills"])}
    output = io.StringIO(); writer = csv.DictWriter(output, fieldnames=fields); writer.writeheader(); writer.writerow(row)
    return output.getvalue().encode("utf-8")

def show_metric_cards(result):
    """Render component scores returned by the hybrid engine without recalculating them."""
    labels = [("ML score", result["ml_score"]), ("Skill match", result["skill_score"]), ("Interest match", result["interest_score"]), ("Education match", result["education_score"])]
    for column, (label, value) in zip(st.columns(4), labels):
        with column: st.metric(label, f"{value:.2f}%", border=True)

def show_recommendation(result):
    st.header("Your recommended career", divider="blue")
    st.subheader(result["career_domain"])
    st.metric("Hybrid match score", f"{result['hybrid_score']:.2f}%", result["recommendation_strength"], border=True)
    show_metric_cards(result)
    left, right = st.columns((1, 1))
    with left:
        st.subheader("Why this career?")
        for reason in result["why"]: st.write(f"✓ {reason}")
    with right:
        st.subheader("Suggested career roles")
        for role in result["career_roles"]: st.write(f"• {role}")
    if result["close_alternatives"]:
        st.info("Close alternatives: " + ", ".join(result["close_alternatives"]))

def show_top_matches(result):
    st.header("Top career matches", divider="blue")
    top_results = result["top_results"]
    chart_data = pd.DataFrame({"Career domain": [item["career_domain"] for item in top_results], "Hybrid score": [item["hybrid_score"] for item in top_results]}).set_index("Career domain")
    st.bar_chart(chart_data)
    for rank, item in enumerate(top_results, 1):
        with st.container(border=True):
            st.subheader(f"#{rank} · {item['career_domain']}")
            st.progress(item["hybrid_score"] / 100, text=f"Hybrid score: {item['hybrid_score']:.2f}%")
            show_metric_cards(item)
            st.caption("Matched skills: " + (", ".join(item["matched_skills"]) or "No direct matches yet"))

def show_skill_gap(result):
    st.header("Skill gap analysis", divider="blue")
    st.metric("Overall skill match", f"{result['skill_match']:.1f}%", border=True)
    st.progress(result["skill_match"] / 100)
    left, right = st.columns(2)
    with left:
        st.subheader("Skills you already have")
        if result["matched_skills"]:
            for skill in result["matched_skills"]: st.success(skill, icon="✅")
        else: st.info("No direct skill matches found yet.")
    with right:
        st.subheader("Skills to improve")
        if result["missing_skills"]:
            for skill in result["missing_skills"]: st.warning(skill, icon="⚠️")
        else: st.success("Excellent — no major missing skills.")
    st.subheader("Recommended skills to learn")
    if result["recommended_skills"]:
        for index, skill in enumerate(result["recommended_skills"], 1): st.write(f"{index}. {skill}")
    else: st.info("Continue building advanced projects and a portfolio.")

def format_roadmap_step(step, index):
    """Clean legacy escaped newlines and remove a duplicated leading step label."""
    del index  # The UI owns numbering; it is intentionally not duplicated in the text.
    cleaned = str(step or "").replace("\\n", "\n").replace("\\\n", "\n")
    cleaned = re.sub(r"\n[ \t]*\+", "\n", cleaned)
    cleaned = re.sub(r"^\s*step\s*\d+\s*[:.\-]?\s*", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

def show_roadmap(result):
    """Render roadmap entries without escaped-newline or duplicate-step artifacts."""
    st.header("Personalized career roadmap", divider="blue")
    st.caption(f"Recommended career: {result['career_domain']}")
    for index, step in enumerate(result["roadmap"], 1):
        with st.container(border=True):
            st.subheader(f"STEP {index}")
            st.write(format_roadmap_step(step, index))

def show_export(profile, result):
    st.header("Export report", divider="blue")
    st.write("Download your current career analysis as a CSV report.")
    st.download_button("Download career report", data=report_csv(profile, result), file_name="careercompass_report.csv", mime="text/csv", icon=":material/download:")

initialise_state()
st.title("🧭 CareerCompass AI")
st.subheader("AI-powered career recommendation & skill development platform")
st.write("Discover career paths based on your skills, interests, education, and AI-powered analysis.")

with st.sidebar:
    st.header("Your profile")
    with st.form("profile_form", border=False):
        age = st.number_input("Age", min_value=15, max_value=100, value=18, step=1, key="profile_age")
        education = st.text_input("Education", placeholder="B.Tech CSE 2nd Year", key="profile_education")
        skills = st.text_area("Skills (comma separated)", placeholder="Python, Networking, Linux, Burp Suite", key="profile_skills")
        interests = st.text_area("Interests (comma separated)", placeholder="Defensive Security, Ethical Hacking", key="profile_interests")
        submitted = st.form_submit_button("Analyze my career", type="primary", icon=":material/rocket_launch:")
    if submitted:
        try:
            valid_age, valid_education, valid_skills, valid_interests = validate_profile(age, education, skills, interests)
            with st.spinner("Analyzing your career profile..."):
                result = recommend_career(valid_age, valid_education, valid_skills, valid_interests, model=get_model())
            st.session_state.profile = {"age": valid_age, "education": valid_education, "skills": valid_skills, "interests": valid_interests}
            st.session_state.analysis = result
            st.success("Career analysis completed.")
        except (ValueError, FileNotFoundError, OSError) as error:
            st.error(f"Unable to analyze this profile: {error}")
        except Exception:
            st.error("An unexpected error occurred while analyzing your profile. Please try again.")

result = st.session_state.analysis
profile = st.session_state.profile
if result is None or profile is None:
    st.info("Welcome to CareerCompass AI. Enter your profile in the sidebar and select Analyze my career.", icon="👋")
else:
    st.caption(f"Current profile · Age {profile['age']} · {profile['education']} · Skills: {', '.join(profile['skills'])}")
    recommendation_tab, matches_tab, skills_tab, roadmap_tab, export_tab = st.tabs(["🏆 Career recommendation", "📊 Top career matches", "🛠 Skill gap analysis", "🗺 Career roadmap", "📥 Export report"])
    with recommendation_tab: show_recommendation(result)
    with matches_tab: show_top_matches(result)
    with skills_tab: show_skill_gap(result)
    with roadmap_tab: show_roadmap(result)
    with export_tab: show_export(profile, result)
