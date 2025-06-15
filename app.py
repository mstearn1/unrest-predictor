# Unrest Prediction Model Web App (Streamlit Version)
# Save this file as app.py and upload to Streamlit Cloud to go live

import streamlit as st
import math

def unrest_probability(econ, polar, justice, social, timing, activists, history):
    Z = (-2.5 +
         1.2 * econ +
         0.9 * polar +
         2.0 * justice +
         1.1 * social +
         1.5 * timing +
         0.8 * activists +
         1.0 * history)
    probability = 1 / (1 + math.exp(-Z))
    return round(probability, 3)

st.set_page_config(page_title="Unrest Predictor", layout="centered")
st.title("🧠 Civil Unrest Prediction Tool")
st.write("Estimate the probability of civil unrest based on local conditions.")

with st.form("input_form"):
    st.subheader("📊 Input Factors (0 to 1 scale)")
    econ = st.slider("Economic Pressure", 0.0, 1.0, 0.5)
    polar = st.slider("Political Polarization", 0.0, 1.0, 0.5)
    justice = st.slider("Justice Trigger (e.g., police incident)", 0.0, 1.0, 0.0)
    social = st.slider("Social Media Virality", 0.0, 1.0, 0.5)
    timing = st.slider("Symbolic Timing (e.g., election, holiday)", 0.0, 1.0, 0.5)
    activists = st.slider("Activist Infrastructure", 0.0, 1.0, 0.5)
    history = st.slider("History of Unrest", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Calculate Risk")

if submitted:
    risk = unrest_probability(econ, polar, justice, social, timing, activists, history)
    st.metric(label="Estimated Probability of Unrest", value=f"{risk * 100:.1f}%")

    if risk > 0.75:
        st.error("⚠️ High Risk of Civil Unrest")
    elif risk > 0.5:
        st.warning("⚠️ Moderate Risk")
    else:
        st.success("✅ Low Risk")

st.markdown("---")
st.caption("Created with 💡 by ChatGPT and [Streamlit](https://streamlit.io)")
