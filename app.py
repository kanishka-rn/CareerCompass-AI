import streamlit as st
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from recommender import recommend_career
from pdf_generator import generate_career_report_pdf


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🧠 CareerCompass AI")
st.subheader("AI-Powered Career Recommendation System")

st.write(
    "Discover suitable career domains, career roles, skill gaps, "
    "and personalized learning roadmaps based on your profile."
)

st.divider()


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Enter your age",
        min_value=15,
        max_value=80,
        value=18
    )

    education = st.text_input(
        "Enter your education",
        placeholder="Example: 2nd Year B.Tech CSE"
    )


with col2:

    skills = st.text_area(
        "Enter your skills",
        placeholder="Example: Python, Java, HTML, CSS, SQL"
    )

    interests = st.text_area(
        "Enter your interests",
        placeholder="Example: Artificial Intelligence, Web Development"
    )


st.divider()


# --------------------------------------------------
# RECOMMEND BUTTON
# --------------------------------------------------

if st.button("🚀 Get Career Recommendation", use_container_width=True):

    if not education or not skills or not interests:

        st.warning(
            "⚠️ Please enter your education, skills, and interests."
        )

    else:

        with st.spinner("🧠 CareerCompass AI is analyzing your profile..."):

            result = recommend_career(
                age,
                education,
                skills,
                interests
            )

        st.success("✅ Career analysis completed!")


        # ------------------------------------------
        # CAREER RESULT
        # ------------------------------------------

        st.divider()

        st.header("🎯 Career Recommendation")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Recommended Career Domain",
                result["career_domain"]
            )

        with col2:

            confidence = result["confidence"] * 100

            st.metric(
                "AI Confidence",
                f"{confidence:.2f}%"
            )


        # ------------------------------------------
        # CAREER ROLES
        # ------------------------------------------

        st.divider()

        st.header("💼 Suggested Career Roles")

        for role in result["career_roles"]:

            st.write(f"• {role}")


        # ------------------------------------------
        # SKILL ANALYSIS
        # ------------------------------------------

        st.divider()

        st.header("📊 Skill Analysis")

        skill_match = result["skill_match"]

        st.progress(
            int(skill_match)
        )

        st.write(
            f"🎯 Overall Skill Match: **{skill_match:.1f}%**"
        )


        # ------------------------------------------
        # SKILLS YOU HAVE
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Skills You Already Have")

            if result["matched_skills"]:

                for skill in result["matched_skills"]:

                    st.write(f"• {skill}")

            else:

                st.write("No strong skill matches found.")


        # ------------------------------------------
        # SKILLS TO IMPROVE
        # ------------------------------------------

        with col2:

            st.subheader("❌ Skills To Improve")

            if result["missing_skills"]:

                for skill in result["missing_skills"]:

                    st.write(f"• {skill}")

            else:

                st.write("Excellent! No major skill gaps detected.")


        # ------------------------------------------
        # RECOMMENDED SKILLS
        # ------------------------------------------

        st.divider()

        st.header("🚀 Recommended Skills To Explore")

        for skill in result["recommended_skills"]:

            st.write(f"• {skill}")


        # ------------------------------------------
        # ROADMAP
        # ------------------------------------------

        st.divider()

        st.header("🛣️ Personalized Career Roadmap")

        for i, step in enumerate(result["roadmap"], start=1):

            st.write(f"### STEP {i}: {step}")

        st.divider()

        st.success(
            "🎉 Keep learning, building projects, and improving your skills!"
        )

        # ------------------------------------------
        # PDF REPORT DOWNLOAD
        # ------------------------------------------

        st.divider()

        st.header("📥 Download Full Career Report")
        st.write(
            "Export your complete profile analysis, domain matches, skill gaps, "
            "and step-by-step roadmap as an official PDF report."
        )

        pdf_bytes = generate_career_report_pdf(
            age=int(age),
            education=education,
            skills=skills,
            interests=interests,
            result=result
        )

        st.download_button(
            label="📄 Download Career Report (PDF)",
            data=pdf_bytes,
            file_name=f"CareerCompass_Report_{result['career_domain'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )