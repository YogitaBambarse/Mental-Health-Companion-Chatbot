import streamlit as st
import json

st.set_page_config(page_title="AI Health Assistant", layout="wide")

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

    st.write("### Your Current Needs")
    goal = st.text_area("Describe your goal (e.g., muscle gain, fat loss, etc.)")

    if st.button("Generate Personalised Meal Plan"):
        if goal:
            st.success(f"Meal plan generated for: {goal}")
            st.write("""
            🍳 Breakfast: Oats + Eggs  
            🍛 Lunch: Rice + Chicken + Veggies  
            🍲 Dinner: Roti + Paneer  
            🥜 Snacks: Nuts & Fruits  
            """)
        else:
            st.warning("Please enter your goal")

    st.write("### Your Health Profile")

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

    if st.button("Calculate health metrics"):
        bmi = calculate_bmi(weight, height)
        calories = calculate_calories(weight, height, age)

        st.subheader("Your Health Results")

        if bmi < 18.5:
            st.warning(f"BMI: {round(bmi,2)} (Underweight)")
        elif bmi < 25:
            st.success(f"BMI: {round(bmi,2)} (Normal weight)")
        else:
            st.error(f"BMI: {round(bmi,2)} (Overweight)")

        st.info(f"Daily Calories: {int(calories)} kcal")

        st.success("👉 Maintain current intake to keep your weight stable.")

# ---------- TAB 3 : AI FITNESS COACH ----------
with tab3:
    st.subheader("AI Fitness Coach")

    st.warning("⚠️ If you have not calculated your BMI, please do it in 'Health Metrics' tab")

    question = st.text_area("Ask your fitness coach")

    if st.button("Get Coaching Advice"):
        if question:
            st.write("### 🧠 Your AI Coach Says:")

            st.write("""
Hello! Based on your goal, here’s your plan:

1. Do strength training 4x/week  
2. Add cardio on weekends  
3. Maintain high protein diet  
4. Stay consistent for 3 months  

You’ll see great results! 💪
            """)
        else:
            st.warning("Please enter a question")
