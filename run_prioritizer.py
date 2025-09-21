# src/app_streamlit.py
import streamlit as st
import pandas as pd
from datetime import datetime
from parser import parse_task
from prioritze import rank_tasks

st.set_page_config(page_title="Assist", layout="wide")
st.title("Smart Task Assistant")

# textarea to paste multiple lines or single task
input_text = st.text_area("Paste tasks (one per line) or type a task:", height=120)

uploaded = st.file_uploader("Or upload a CSV file with a 'task' column", type=["csv"])
tasks = []

if uploaded:
    df = pd.read_csv(uploaded)
    if 'task' in df.columns:
        tasks = df['task'].astype(str).tolist()
    else:
        st.error("CSV must contain a 'task' column")

if input_text:
    tasks += [line.strip() for line in input_text.splitlines() if line.strip()]

if st.button("Parse & Rank"):
    if not tasks:
        st.info("Add tasks via text area or upload a CSV.")
    else:
        parsed = [parse_task(t) for t in tasks]
        ranked = rank_tasks(parsed, ref=datetime.now())
        rows = []
        for score, t in ranked:
            rows.append({
                'score': round(float(score), 4),
                'title': t.get('title'),
                'due': t.get('due'),
                'est_minutes': t.get('est_minutes'),
                'importance': t.get('importance'),
                'raw': t.get('raw')
            })
        st.table(pd.DataFrame(rows))
        csv = pd.DataFrame(rows).to_csv(index=False)
        st.download_button("Download CSV", csv, file_name="tasks_ranked.csv")
