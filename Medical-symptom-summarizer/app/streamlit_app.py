"""
streamlit_app.py
Main Streamlit UI for the Medical Symptom Summarizer.
"""

import json
import time
import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from prompt_builder import SYSTEM_PROMPT, build_user_message
from validator import validate_response, SymptomSummary
from pydantic import ValidationError

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
)

TRIAGE_COLOURS = {
    "low":      ("🟢", "#d4edda", "#155724"),
    "moderate": ("🟡", "#fff3cd", "#856404"),
    "high":     ("🔴", "#f8d7da", "#721c24"),
}

MAX_RETRIES = 3


def call_api(symptom_text: str) -> SymptomSummary:
    """Call Gemini with retry on failure."""
    user_msg = build_user_message(symptom_text)
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(user_msg)
            # Clean response - remove markdown code fences if present
            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[1]  # Remove first line
                raw_text = raw_text.rsplit("```", 1)[0]  # Remove last ```
            raw = json.loads(raw_text)
            return validate_response(raw)
        except ValidationError as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(2 ** attempt)


# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Medical Symptom Summarizer",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Medical Symptom Summarizer")
st.warning(
    "⚠️ **Disclaimer:** This tool does not provide medical advice or diagnosis. "
    "All outputs require clinical judgment by a qualified professional."
)

# ── Layout ─────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.subheader("Patient Symptom Description")
    symptom_text = st.text_area(
        label="Paste or type the patient's description",
        height=250,
        placeholder="e.g. I've had a severe headache for 2 days, pain is 8/10, light makes it worse...",
    )
    submitted = st.button("🔍 Summarise", type="primary", use_container_width=True)

    # Session history (last 5)
    if "history" not in st.session_state:
        st.session_state.history = []

    if st.session_state.history:
        st.markdown("---")
        st.caption("Recent summaries (this session)")
        for item in reversed(st.session_state.history[-5:]):
            st.caption(f"• {item['chief_complaint']} — **{item['triage_level'].upper()}**")

with col_output:
    st.subheader("Structured Summary")

    if submitted:
        if not symptom_text.strip():
            st.error("Please enter a symptom description.")
        elif len(symptom_text.strip().split()) < 5:
            st.warning("Description is very short. Please provide more detail for accurate summarisation.")
        else:
            with st.spinner("Analysing symptoms..."):
                try:
                    result = call_api(symptom_text)

                    # Triage badge
                    icon, bg, fg = TRIAGE_COLOURS[result.triage_level]
                    st.markdown(
                        f"""<div style='background:{bg};color:{fg};padding:12px 18px;
                        border-radius:8px;font-weight:bold;font-size:1.1rem;margin-bottom:16px'>
                        {icon} Triage Level: {result.triage_level.upper()}</div>""",
                        unsafe_allow_html=True,
                    )

                    # Fields
                    st.markdown(f"**Chief Complaint:** {result.chief_complaint}")
                    st.markdown(f"**Onset:** {result.onset or 'Not mentioned'}")
                    st.markdown(f"**Duration:** {result.duration or 'Not mentioned'}")
                    st.markdown(f"**Severity:** {result.severity or 'Not mentioned'}/10")

                    if result.red_flags:
                        st.markdown("**🚨 Red Flags:**")
                        for flag in result.red_flags:
                            st.markdown(f"- {flag}")
                    else:
                        st.markdown("**Red Flags:** None identified")

                    # Export
                    st.download_button(
                        label="⬇ Export as JSON",
                        data=result.model_dump_json(indent=2),
                        file_name="symptom_summary.json",
                        mime="application/json",
                    )

                    # Save to session history
                    st.session_state.history.append(result.model_dump())

                except ValidationError as e:
                    st.error(f"Output validation failed: {e}")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
