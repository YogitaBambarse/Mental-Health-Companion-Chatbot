import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Health Companion", layout="wide")

# ---------------- ENV ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ---------------- USER STORAGE ----------------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login / Register")

    option = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if option == "Register":
            if username not in users:
                users[username] = {"password": password, "history": []}
                save_users(users)
                st.success("Registered successfully! Please login.")
            else:
                st.warning("Username already exists.")
        else:
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ---------------- MAIN APP ----------------
st.title("🤖 AI Health Companion")

st.sidebar.header("User Details")

weight = st.sidebar.number_input("Weight (kg)", 30, 150, 60)
height = st.sidebar.number_input("Height (cm)", 120, 210, 165)
age = st.sidebar.number_input("Age", 10, 80, 22)

medical = st.sidebar.text_area("Medical Conditions", "None")
food_pref = st.sidebar.text_area("Food Preferences", "Veg")
diet_restrict = st.sidebar.text_area("Dietary Restrictions", "None")

bmi = weight / ((height/100)**2)
calories = 22 * weight

st.sidebar.success(f"BMI: {round(bmi,2)}")
st.sidebar.info(f"Estimated Calories: {int(calories)} kcal")

tabs = st.tabs(["🍽 Daily Plan", "📅 Weekly Plan", "📊 Calorie Chart", "📜 History"])

# ---------------- DAILY PLAN ----------------
with tabs[0]:
    st.subheader("Generate Daily Meal Plan")

    if st.button("Generate Daily Plan"):
        if not api_key:
            st.error("API Key not found")
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Create a personalized daily Indian diet plan.
                Age: {age}
                Weight: {weight} kg
                Height: {height} cm
                BMI: {round(bmi,2)}
                Medical Conditions: {medical}
                Food Preference: {food_pref}
                Dietary Restrictions: {diet_restrict}
                Target Calories: {calories}
                """

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                st.success("AI Plan Generated ✅")
                st.write(response.text)

                users[st.session_state.username]["history"].append(response.text)
                save_users(users)

            except Exception as e:
                st.error("AI Error")
                st.write(str(e))

# ---------------- WEEKLY PLAN ----------------
with tabs[1]:
    st.subheader("Generate Weekly Meal Plan")

    if st.button("Generate Weekly Plan"):
        if not api_key:
            st.error("API Key not found")
        else:
            try:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                Create a personalized 7-day Indian diet plan.
                Age: {age}
                Weight: {weight} kg
                Height: {height} cm
                BMI: {round(bmi,2)}
                Medical Conditions: {medical}
                Food Preference: {food_pref}
                Dietary Restrictions: {diet_restrict}
                Target Calories: {calories}
                """

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                st.success("AI Weekly Plan Generated ✅")
                st.write(response.text)

                users[st.session_state.username]["history"].append(response.text)
                save_users(users)

            except Exception as e:
                st.error("AI Error")
                st.write(str(e))

# ---------------- CALORIE CHART ----------------
with tabs[2]:
    st.subheader("Calorie Breakdown")

    breakfast = calories * 0.25
    lunch = calories * 0.35
    snacks = calories * 0.15
    dinner = calories * 0.25

    labels = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    values = [breakfast, lunch, snacks, dinner]

    fig = plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig)

# ---------------- HISTORY ----------------
with tabs[3]:
    st.subheader("Your Previous Meal Plans")

    history = users[st.session_state.username]["history"]

    if history:
        for i, item in enumerate(history):
            st.markdown(f"### Plan {i+1}")
            st.write(item)
    else:
        st.info("No meal plans generated yet.")

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()