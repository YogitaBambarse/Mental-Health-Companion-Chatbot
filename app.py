import streamlit as st
import json
import matplotlib.pyplot as plt
import requests
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- AI FUNCTION (FIXED) ----------
def get_ai_response(prompt):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        data = response.json()

        # Handle different response formats
        if isinstance(data, list):
            return data[0].get("generated_text", "No response")

        elif isinstance(data, dict):
            if "error" in data:
                return f"❌ HF Error: {data['error']}"
            else:
                return "❌ Unexpected response"

        else:
            return "❌ Unknown response"

    except Exception as e:
        return f"❌ Error: {str(e)}"

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

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Personalised Meal Planning")

    goal = st.text_area("Describe your goal")

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
            st.warning("Enter your goal")

    st.subheader("Your Health Profile")

    profile = {
        "goal": "Fitness",
        "dietPreference": "Veg",
        "condition": "Beginner",
        "preferences": ["High protein", "Low sugar"]
    }

    st.code(json.dumps(profile, indent=2), language="json")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Health Metrics")

    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input("Height (cm)", 150, 220, 170)
        weight = st.number_input("Weight (kg)", 40, 120, 70)
        age = st.number_input("Age", 10, 80, 25)

    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])

    def bmi_calc(w, h):
        return w / ((h/100) ** 2)

    def calorie_calc(w, h, a):
        return 10*w + 6.25*h - 5*a + 5

    if st.button("Calculate Metrics"):
        bmi = bmi_calc(weight, height)
        cal = calorie_calc(weight, height, age)

        if bmi < 18.5:
            st.warning(f"BMI: {round(bmi,2)} (Underweight)")
        elif bmi < 25:
            st.success(f"BMI: {round(bmi,2)} (Normal)")
        else:
            st.error(f"BMI: {round(bmi,2)} (Overweight)")

        st.info(f"Calories: {int(cal)} kcal")

    # GRAPH
    st.subheader("📊 Progress Tracker")

    weights = st.text_input("Enter weights", "70,69,68,67")

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
    st.subheader("AI Fitness Coach (FREE)")

    q = st.text_area("Ask your question")

    if st.button("Get Advice"):
        if q:
            with st.spinner("Thinking..."):
                ans = get_ai_response(q)
                st.write("### 🧠 AI Coach Says:")
                st.success(ans)
        else:
            st.warning("Enter question")