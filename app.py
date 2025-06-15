# Unrest Prediction Model Web App (Streamlit Version)
# Save this file as app.py and upload to Streamlit Cloud to go live

import streamlit as st
import math

# City presets for unrest model inputs (values between 0 and 1)
city_presets = {
    "Los Angeles":       [0.6, 0.7, 0.8, 0.75, 0.6, 0.7, 0.9],
    "New York":          [0.7, 0.8, 0.9, 0.8, 0.7, 0.7, 0.85],
    "Washington DC":     [0.65, 0.85, 0.9, 0.7, 0.75, 0.8, 0.8],
    "Boston":            [0.55, 0.6, 0.4, 0.5, 0.4, 0.6, 0.3],
    "Miami":             [0.7, 0.6, 0.7, 0.6, 0.5, 0.5, 0.6],
    "Dallas":            [0.5, 0.55, 0.3, 0.4, 0.35, 0.4, 0.3],
    "Phoenix":           [0.6, 0.5, 0.4, 0.45, 0.4, 0.4, 0.35],
    "Seattle":           [0.6, 0.7, 0.8, 0.7, 0.6, 0.65, 0.8],
    "San Francisco":     [0.65, 0.75, 0.85, 0.8, 0.65, 0.75, 0.9],
}

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
    st.subheader("🌍 Choose City or Enter Custom Values")

    city = st.selectbox("Select a City", ["Custom"] + list(city_presets.keys()))

    if city != "Custom":
        econ, polar, justice, social, timing, activists, history = city_presets[city]
    else:
        econ = polar = justice = social = timing = activists = history = 0.5

    econ = st.slider("Economic Pressure", 0.0, 1.0, econ)
    polar = st.slider("Political Polarization", 0.0, 1.0, polar)
    justice = st.slider("Justice Trigger (e.g., police incident)", 0.0, 1.0, justice)
    social = st.slider("Social Media Virality", 0.0, 1.0, social)
    timing = st.slider("Symbolic Timing (e.g., election, holiday)", 0.0, 1.0, timing)
    activists = st.slider("Activist Infrastructure", 0.0, 1.0, activists)
    history = st.slider("History of Unrest", 0.0, 1.0, history)

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

