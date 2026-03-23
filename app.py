import streamlit as st
import json
import matplotlib.pyplot as plt
import os
from openai import OpenAI

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- API (SECURE) ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional fitness coach. Give structured, practical advice."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

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
tab1, tab2, tab3 = st.tabs(["🍽 Meal Planning", "📊 Health Metrics", "🏋️ AI Fitness Coach"])

# ---------- TAB 1 : MEAL PLANNING ----------
with tab1:
    st.subheader("Personalised Meal Planning")

    goal = st.text_area("Describe your goal (muscle gain, fat loss, etc.)")

    if st.button("Generate Meal Plan"):
        if goal:
            st.success(f"Plan for: {goal}")
            st.write("""
🍳 Breakfast: Oats + Eggs  
🍛 Lunch: Rice + Chicken + Veggies  
🍲 Dinner: Roti + Paneer  
🥜 Snacks: Nuts & Fruits  
""")
        else:
            st.warning("Enter your goal")

    st.subheader("Your Health Profile")

    profile = {
        "goal": "Muscle gain",
        "dietPreference": "Veg",
        "condition": "Beginner",
        "preferences": ["High protein", "Low sugar"]
    }

    st.code(json.dumps(profile, indent=2), language="json")

# ---------- TAB 2 : HEALTH METRICS ----------
with tab2:
    st.subheader("Health Metrics and Calorie Calculator")

    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input("Height (cm)", value=170)
        weight = st.number_input("Weight (kg)", value=70)
        age = st.number_input("Age", value=25)

    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

    def calculate_bmi(weight, height):
        h = height / 100
        return weight / (h * h)

    def calculate_calories(weight, height, age):
        return 10*weight + 6.25*height - 5*age + 5

    if st.button("Calculate Metrics"):
        bmi = calculate_bmi(weight, height)
        calories = calculate_calories(weight, height, age)

        st.subheader("Your Results")

        if bmi < 18.5:
            st.warning(f"BMI: {round(bmi,2)} (Underweight)")
        elif bmi < 25:
            st.success(f"BMI: {round(bmi,2)} (Normal)")
        else:
            st.error(f"BMI: {round(bmi,2)} (Overweight)")

        st.info(f"Daily Calories: {int(calories)} kcal")

    # ---------- GRAPH ----------
    st.subheader("📊 Weight Progress Tracker")

    weights = st.text_input("Enter weights (comma separated)", "70,69,68,67")

    if st.button("Show Graph"):
        try:
            weight_list = list(map(float, weights.split(",")))

            plt.figure()
            plt.plot(weight_list, marker='o')
            plt.xlabel("Days")
            plt.ylabel("Weight (kg)")
            plt.title("Progress")

            st.pyplot(plt)
        except:
            st.error("Please enter valid numbers separated by commas")

# ---------- TAB 3 : AI COACH ----------
with tab3:
    st.subheader("AI Fitness Coach")

    question = st.text_area("Ask your fitness coach")

    if st.button("Get AI Advice"):
        if question:
            with st.spinner("Thinking..."):
                try:
                    reply = get_ai_response(question)
                    st.write("### 🧠 AI Coach Says:")
                    st.write(reply)
                except Exception as e:
                    st.error("Error fetching AI response. Check API key.")
        else:
            st.warning("Enter a question")