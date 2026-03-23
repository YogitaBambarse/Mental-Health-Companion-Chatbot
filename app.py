import streamlit as st
import requests
import os
import time

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Health Assistant", layout="wide")

# ---------- SIDEBAR ----------
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

    # fallback
    return "⚠️ AI busy... showing basic suggestion:\n- Stay active\n- Eat healthy\n- Stay hydrated 💪"

# ---------- TITLE ----------
st.title("🧠 AI Personal Health & Fitness Assistant")
st.caption("Smart nutrition • Intelligent fitness • Personalized health insights")

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "🍽 Meal Plan",
    "🍎 Food Analysis",
    "🏋️ AI Coach",
    "📊 Health Insights"
])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Meal Plan")

    if st.button("Generate Plan"):
        if goal == "Weight Loss":
            st.success("🔥 Weight Loss Diet")
            st.write("Oats • Salad • Soup • Fruits")

        elif goal == "Muscle Gain":
            st.success("💪 Muscle Gain Diet")
            st.write("Eggs • Rice • Paneer • Milk")

        else:
            st.success("✨ Balanced Diet")
            st.write("Dal • Roti • Veg • Fruits")

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Food Analysis")

    food = st.text_input("Enter food")

    if st.button("Analyze"):
        if food:
            prompt = f"Give nutrition info of {food}"
            with st.spinner("Analyzing..."):
                result = get_ai_response(prompt)
            st.success(result)
        else:
            st.warning("Enter food")

# ---------- TAB 3 (COACH BACK) ----------
with tab3:
    st.subheader("🏋️ AI Fitness Coach")

    question = st.text_area("Ask your coach")

    if st.button("Get Advice"):
        if question:
            with st.spinner("Thinking..."):
                reply = get_ai_response(question)
            st.success(reply)
        else:
            st.warning("Ask something")

# ---------- TAB 4 ----------
with tab4:
    st.subheader("Health Insights")

    def bmi(w, h):
        return w / ((h/100)**2)

    if st.button("Check Health"):
        b = bmi(weight, height)

        if b < 18.5:
            st.warning(f"BMI: {round(b,2)} (Underweight)")
        elif b < 25:
            st.success(f"BMI: {round(b,2)} (Normal)")
        else:
            st.error(f"BMI: {round(b,2)} (Overweight)")

        st.info("Stay active • Eat healthy • Sleep well")