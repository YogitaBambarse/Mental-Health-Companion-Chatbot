import streamlit as st
import requests
import os
import time

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- SIDEBAR (PROFILE) ----------
st.sidebar.header("👤 Your Profile")

age = st.sidebar.number_input("Age", 10, 80, 25)
height = st.sidebar.number_input("Height (cm)", 140, 220, 170)
weight = st.sidebar.number_input("Weight (kg)", 40, 120, 70)

goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Maintain Fitness"])
diet = st.sidebar.selectbox("Diet Preference", ["Veg", "Non-Veg"])
activity = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

# ---------- AI FUNCTION ----------
def get_ai_response(prompt):
    API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

        if response.text:
            try:
                data = response.json()

                if isinstance(data, list):
                    return data[0].get("generated_text", "No response")

                elif isinstance(data, dict) and "error" in data:
                    if "loading" in data["error"].lower():
                        time.sleep(5)
                    else:
                        return f"❌ {data['error']}"

            except:
                pass
    except:
        pass

    # ---------- FALLBACK ----------
    return "⚠️ Using smart local suggestions (AI temporarily unavailable)"

# ---------- TITLE ----------
st.title("🧠 AI Personal Health & Fitness Assistant")
st.caption("Smart nutrition • Intelligent fitness • Personalized health insights")

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["🍽 Meal Plan", "🍎 Food Analysis", "📊 Health Insights"])

# ---------- TAB 1 : MEAL PLAN ----------
with tab1:
    st.subheader("🍽 Personalized Meal Plan")

    if st.button("Generate Plan"):

        if goal == "Weight Loss":
            st.success("🔥 Weight Loss Diet")
            st.write("""
Breakfast: Oats + Fruits  
Lunch: Dal + Roti + Salad  
Dinner: Soup + Veggies  
Snacks: Nuts  
""")

        elif goal == "Muscle Gain":
            st.success("💪 Muscle Gain Diet")
            st.write("""
Breakfast: Eggs + Milk  
Lunch: Rice + Chicken / Paneer  
Dinner: Roti + Dal  
Snacks: Protein rich foods  
""")

        else:
            st.success("✨ Balanced Diet")
            st.write("""
Breakfast: Fruits + Milk  
Lunch: Dal + Rice  
Dinner: Roti + Veg  
Snacks: Nuts  
""")

# ---------- TAB 2 : FOOD ANALYSIS ----------
with tab2:
    st.subheader("🍎 Food Analysis")

    food = st.text_input("Enter food item (e.g. Pizza, Salad, Burger)")

    if st.button("Analyze Food"):
        if food:
            prompt = f"Give nutrition analysis of {food} in simple points"

            with st.spinner("Analyzing..."):
                result = get_ai_response(prompt)

            st.success(result)

        else:
            st.warning("Enter food item")

# ---------- TAB 3 : HEALTH INSIGHTS ----------
with tab3:
    st.subheader("📊 Health Insights")

    def bmi(w, h):
        return w / ((h/100)**2)

    if st.button("Check Health"):

        b = bmi(weight, height)

        if b < 18.5:
            st.warning(f"BMI: {round(b,2)} (Underweight)")
            st.info("Increase calorie intake and protein.")

        elif b < 25:
            st.success(f"BMI: {round(b,2)} (Normal)")
            st.info("Maintain your healthy lifestyle 👍")

        else:
            st.error(f"BMI: {round(b,2)} (Overweight)")
            st.info("Focus on cardio & diet control.")

        st.markdown("### 💡 Suggestions")
        st.write("""
- Drink 3-4L water  
- Exercise regularly  
- Sleep 7-8 hrs  
- Avoid junk food  
""")