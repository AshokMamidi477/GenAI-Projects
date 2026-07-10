"""dashboard.py — Streamlit support queue"""

import os, glob
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Support Queue", page_icon="📧", layout="wide")
st.title("📧 Customer Support Queue Dashboard")

# Find all CSV files in the output folder, sorted newest first
csv_files = sorted(glob.glob("output/*.csv"), reverse=True)

if not csv_files:
    # Fall back to sample data if no real run has happened yet
    sample = "samples/sample_classified_output.csv"
    if os.path.exists(sample):
        df = pd.read_csv(sample)
        st.caption("Showing sample data — run classifier.py to load live data")
    else:
        st.warning("No data found. Run src/classifier.py first.")
        st.stop()   # st.stop() halts execution — nothing below this runs
else:
    df = pd.read_csv(csv_files[0])   # Load only the most recent file
    st.caption(f"Latest run: `{csv_files[0]}`")

    # 4 columns side by side — one per urgency level
cols = st.columns(4)
for col, level, icon in zip(cols, ["critical", "high", "medium", "low"], ["🔴", "🟠", "🟡", "🟢"]):
    count = int((df.get("urgency", "") == level).sum()) if "urgency" in df.columns else 0
    col.metric(f"{icon} {level.capitalize()}", count)

    # Optional filter for chargeback risk
if st.checkbox("Show chargeback risk only") and "chargeback_risk" in df.columns:
    df = df[df["chargeback_risk"] == True]

# Show the dataframe as an interactive table
st.dataframe(df, use_container_width=True)

# Let support agents download the filtered view
st.download_button("Download CSV", df.to_csv(index=False), "queue.csv", "text/csv")