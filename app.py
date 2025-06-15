# Updated Unrest Predictor with History & News

import streamlit as st
import math
import json
import datetime
import requests

# 1. City presets (with updated polarization from 2024 election surveys)
city_presets = {
    "Los Angeles":       [0.6, 0.8, 0.8, 0.75, 0.6, 0.7, 0.9],
    "New York":          [0.7, 0.85, 0.9, 0.8, 0.7, 0.7, 0.85],
    "Washington DC":     [0.65, 0.9, 0.9, 0.7, 0.75, 0.8, 0.8],
    "Boston":            [0.55, 0.75, 0.4, 0.5, 0.4, 0.6, 0.3],
    "Miami":             [0.7, 0.7, 0.7, 0.6, 0.5, 0.5, 0.6],
    "Dallas":            [0.5, 0.65, 0.3, 0.4, 0.35, 0.4, 0.3],
    "Phoenix":           [0.6, 0.7, 0.4, 0.45, 0.4, 0.4, 0.35],
    "Seattle":           [0.6, 0.8, 0.8, 0.7, 0.6, 0.65, 0.8],
    "San Francisco":     [0.65, 0.85, 0.85, 0.8, 0.65, 0.75, 0.9],
}

def unrest_probability(e, p, j, s, t, a, h):
    Z = (-2.5 + 1.2*e + 0.9*p + 2.0*j + 1.1*s + 1.5*t + 0.8*a + 1.0*h)
    return round(1/(1+math.exp(-Z)), 3)

# Initialize history log
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Unrest Predictor", layout="wide")
st.title("🧠 Civil Unrest Prediction Tool")
st.write("Select a city, tweak parameters, and see how the risk changes in real time.")

# Input form
with st.form("input_form"):
    st.subheader("🌍 City or Custom Entry")
    city = st.selectbox("Select City", ["Custom"] + list(city_presets))
    
    if city != "Custom":
        e, p, j, s, t, a, h = city_presets[city]
    else:
        e = p = j = s = t = a = h = 0.5
    
    e = st.slider("Economic Pressure", 0.0,1.0,e)
    p = st.slider("Political Polarization", 0.0,1.0,p)
    j = st.slider("Justice Trigger", 0.0,1.0,j)
    s = st.slider("Social Media Virality", 0.0,1.0,s)
    t = st.slider("Symbolic Timing", 0.0,1.0,t)
    a = st.slider("Activist Infrastructure", 0.0,1.0,a)
    h = st.slider("History of Unrest", 0.0,1.0,h)

    if st.form_submit_button("Calculate Risk"):
        risk = unrest_probability(e,p,j,s,t,a,h)
        st.metric("Estimated Probability of Unrest", f"{risk*100:.1f}%")
        # Risk assessment
        if risk > 0.75:
            st.error("⚠️ High Risk")
        elif risk > 0.5:
            st.warning("⚠️ Moderate Risk")
        else:
            st.success("✅ Low Risk")
        # Log to history
        st.session_state.history.append({
            "date": datetime.date.today().isoformat(),
            "city": city,
            "risk": risk
        })

# 2. History Tracker
st.markdown("### 📈 Prediction History")
st.json(st.session_state.history)

# 3. Live News Feed (NYT example via RSS)
st.markdown("### 📰 Recent News")
rss_feed = "https://rss.nytimes.com/services/xml/rss/nyt/US.xml"  # example feed
try:
    import feedparser
    news = feedparser.parse(rss_feed)
    for entry in news.entries[:5]:
        st.write(f"- [{entry.title}]({entry.link})")
except ModuleNotFoundError:
    st.write("Feed parser not installed; news feature disabled.")

st.markdown("---")
st.caption("Updated version with history & news. Created by ChatGPT.")
