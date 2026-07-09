"""app.py — Streamlit UI"""

import os
from datetime import date, timedelta

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from prompt_builder import build_study_plan_prompt, calculate_weeks
from notion_writer import save_plan_to_notion


load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Gemini model
model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite"
)


# Streamlit configuration
st.set_page_config(
    page_title="Study Plan Builder",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Personalized Study Plan Builder")


# -------------------------------
# Session State
# -------------------------------

if "plan_md" not in st.session_state:
    st.session_state.plan_md = None

if "topic" not in st.session_state:
    st.session_state.topic = None

if "target" not in st.session_state:
    st.session_state.target = None


# -------------------------------
# User Input Form
# -------------------------------

with st.form("plan_form"):

    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input(
            "Topic *",
            placeholder="e.g. Machine Learning with Python"
        )

        level = st.selectbox(
            "Current Level",
            [
                "Complete Beginner",
                "Some Familiarity",
                "Intermediate"
            ]
        )

        hours = st.slider(
            "Hours per week",
            2,
            40,
            8
        )

    with col2:

        target = st.date_input(
            "Target date",
            value=date.today() + timedelta(weeks=12)
        )

        resources = st.multiselect(
            "Preferred resources",
            [
                "Books",
                "Video courses",
                "Hands-on projects",
                "Online courses",
                "Podcasts",
                "Articles"
            ]
        )

        goal = st.text_input(
            "Learning goal *",
            placeholder="e.g. Get a junior data analyst job"
        )


    submitted = st.form_submit_button(
        "Generate My Study Plan",
        use_container_width=True
    )


# -------------------------------
# Generate Study Plan
# -------------------------------

if submitted:

    if not topic.strip() or not goal.strip():
        st.error("Please fill in Topic and Learning Goal.")
        st.stop()


    weeks = calculate_weeks(target)


    if weeks < 2:
        st.warning(
            f"Only {weeks} week(s) to target — consider extending your deadline."
        )


    with st.spinner(
        f"Designing your {weeks}-week curriculum..."
    ):

        prompt, _ = build_study_plan_prompt(
            topic,
            level,
            hours,
            target,
            resources,
            goal
        )


        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.6,
                max_output_tokens=4096
            )
        )


        # Save generated plan in Streamlit memory
        st.session_state.plan_md = response.text
        st.session_state.topic = topic
        st.session_state.target = target


    st.success(
        f"Your {weeks}-week plan is ready!"
    )


# -------------------------------
# Display Plan
# -------------------------------

if st.session_state.plan_md:

    st.markdown(
        st.session_state.plan_md
    )


    col_a, col_b = st.columns(2)


    with col_a:

        st.download_button(
            "Download as Markdown",
            st.session_state.plan_md,
            file_name=f"{st.session_state.topic.replace(' ', '_')}_plan.md",
            mime="text/markdown"
        )


    with col_b:

        if st.button(
            "Save to Notion",
            use_container_width=True
        ):

            with st.spinner(
                "Saving to Notion..."
            ):

                try:

                    url = save_plan_to_notion(
                        st.session_state.topic,
                        st.session_state.target,
                        st.session_state.plan_md
                    )


                    st.success(
                        "Study plan saved successfully!"
                    )

                    if url:
                        st.markdown(
                            f"[Open in Notion]({url})"
                        )


                except Exception as e:

                    st.error(
                        f"Failed to save to Notion: {e}"
                    )