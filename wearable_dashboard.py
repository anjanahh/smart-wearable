# wearable_dashboard.py

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- Connect to database ---
conn = sqlite3.connect("wearable_data.db")
df = pd.read_sql_query("SELECT * FROM health_data", conn)
conn.close()

st.set_page_config(page_title="Smart Wearable Dashboard", layout="wide")
st.title("📱 Smart Wearable Dashboard")

# --- Summary Stats ---
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)

col1.metric("❤️ Avg Heart Rate", f"{df['heart_rate'].mean():.1f} bpm")
col2.metric("🚶 Total Steps", f"{df['steps'].sum()}")
col3.metric("😴 Avg Sleep", f"{df['sleep_hours'].mean():.1f} hrs")

# --- Line Charts ---
st.subheader("📈 Trends Over Time")

tab1, tab2, tab3 = st.tabs(["Heart Rate", "Steps", "Sleep"])

with tab1:
    st.line_chart(df.set_index("timestamp")["heart_rate"])

with tab2:
    st.line_chart(df.set_index("timestamp")["steps"])

with tab3:
    st.line_chart(df.set_index("timestamp")["sleep_hours"])

# --- Alerts ---
st.subheader("⚠️ Health Alerts")
high_hr = df[df["heart_rate"] > 100]
low_spo2 = df[df["spo2"] < 95]

if not high_hr.empty:
    st.error(f"High Heart Rate Detected {len(high_hr)} times! 🚨")

if not low_spo2.empty:
    st.warning(f"Low SpO₂ Detected {len(low_spo2)} times! ⚠️")

if high_hr.empty and low_spo2.empty:
    st.success("All health readings look normal ✅")
