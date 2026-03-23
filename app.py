import streamlit as st
import json
import matplotlib.pyplot as plt
import requests
import os
import time

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.header("👤 Your Profile")

height = st.sidebar.number_input("Height (cm)", 150, 220, 170)
weight = st.sidebar.number_input("Weight (kg)", 40, 120, 70)
age = st.sidebar.number_input("Age", 10, 80, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

# ---------- HUGGING FACE AI (AUTO RETRY FIX) ----------
def get_ai_response(prompt):
    API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    for i in range(2):  # retry 2 times
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

            if not response.text:
                return "⚠️ Empty response. Try again."

            data = response.json()

            if isinstance(data, list):
                return data[0].get("generated_text", "No response")

            elif isinstance(data, dict):
                if "error" in data:
                    if "loading" in data["error"].lower():
                        time.sleep(5)
                        continue
                    return f"❌ {data['error']}"
                else:
                    return "⚠️ Unexpected response"

            else:
                return "⚠️ Unknown response"

        except Exception as e:
            return f"❌ Error: {str(e)}"

    return "⚠️ Model still loading, try again ⏳"

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🧠 AI Personal Health & Fitness Assistant")
st.caption("Smart nutrition • Intelligent fitness • Personalized health insights")

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(["🍽 Meal Planning", "📊 Health Metrics", "🏋️ AI Fitness Coach", "📅 Weekly Plan"])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Meal Planning")

    goal = st.text_area("Enter your goal")

    if st.button("Generate Meal Plan"):
        if goal:
            st.success(f"Plan for: {goal}")
            st.write("""
🍳 Breakfast: Oats + Eggs  
🍛 Lunch: Rice + Dal + Veggies  
🍲 Dinner: Roti + Paneer  
🥜 Snacks: Fruits & Nuts  
""")
        else:
            st.warning("Enter goal")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Health Metrics")

    def bmi(w, h):
        return w / ((h/100)**2)

    if st.button("Calculate"):
        b = bmi(weight, height)

        if b < 18.5:
            st.warning(f"BMI: {round(b,2)} (Underweight)")
        elif b < 25:
            st.success(f"BMI: {round(b,2)} (Normal)")
        else:
            st.error(f"BMI: {round(b,2)} (Overweight)")

    st.subheader("📊 Progress Graph")

    weights = st.text_input("Enter weights", "70,69,68")

    if st.button("Show Graph"):
        try:
            data = list(map(float, weights.split(",")))
            plt.figure()
            plt.plot(data, marker='o')
            plt.xlabel("Days")
            plt.ylabel("Weight")
            plt.title("Progress")
            st.pyplot(plt)
        except:
            st.error("Invalid input")

# ---------- TAB 3 ----------
with tab3:
    st.subheader("AI Fitness Coach")

    q = st.text_area("Ask something")

    if st.button("Get Advice"):
        if q:
            with st.spinner("Thinking..."):
                ans = get_ai_response(q)
                st.write("### 🧠 AI Says:")
                st.success(ans)
        else:
            st.warning("Enter question")

# ---------- TAB 4 ----------
with tab4:
    st.subheader("📅 Weekly Plan")

    goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain", "General Fitness"])

    if st.button("Generate Weekly Plan"):

        if goal == "Weight Loss":
            st.success("🔥 Weight Loss Plan")
            st.write("""
Mon: Cardio  
Tue: Strength  
Wed: Running  
Thu: Workout  
Fri: HIIT  
Sat: Yoga  
Sun: Rest  
""")

        elif goal == "Muscle Gain":
            st.success("💪 Muscle Plan")
            st.write("""
Mon: Chest  
Tue: Back  
Wed: Legs  
Thu: Shoulder  
Fri: Full Body  
Sat: Cardio  
Sun: Rest  
""")

        else:
            st.success("✨ Fitness Plan")
            st.write("""
Mon: Cardio  
Tue: Strength  
Wed: Yoga  
Thu: Cardio  
Fri: Strength  
Sat: Outdoor  
Sun: Rest  
""")