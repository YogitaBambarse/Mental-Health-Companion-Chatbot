import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import tempfile

# ---------------- ENV ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# ---------------- BASIC LOGIN SYSTEM ----------------
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login / Register")

    choice = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if choice == "Register":
            users[username] = {"password": password, "history": []}
            save_users(users)
            st.success("Registered Successfully! Please login.")
        else:
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.stop()

# ---------------- MAIN APP ----------------
st.set_page_config(page_title="AI Health Companion", layout="wide")
st.title("🤖 AI Health Companion")

# Sidebar
weight = st.sidebar.number_input("Weight (kg)", 30, 150, 60)
height = st.sidebar.number_input("Height (cm)", 120, 210, 165)
age = st.sidebar.number_input("Age", 10, 80, 22)

medical = st.sidebar.text_area("Medical Conditions", "None")
food_pref = st.sidebar.text_area("Food Preferences", "Veg")
diet_restrict = st.sidebar.text_area("Dietary Restrictions", "None")

bmi = weight / ((height/100)**2)
calories = 22 * weight

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🍽 AI Meal Plan", "📊 Calorie Chart", "📅 Weekly Planner", "📜 History"]
)

# ---------------- AI MEAL PLAN ----------------
with tab1:
    if st.button("Generate AI Meal Plan"):
        if api_key:
            prompt = f"""
            Create a detailed one-day Indian meal plan.
            Age: {age}
            Weight: {weight}
            BMI: {round(bmi,2)}
            Medical Conditions: {medical}
            Food Preferences: {food_pref}
            Dietary Restrictions: {diet_restrict}
            Calories Target: {round(calories)}
            """

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            st.write(response.text)

            users[st.session_state.username]["history"].append(response.text)
            save_users(users)

        else:
            st.error("API Key Missing")

# ---------------- CALORIE CHART ----------------
with tab2:
    st.subheader("Calorie Distribution")

    breakfast = calories * 0.25
    lunch = calories * 0.35
    snacks = calories * 0.15
    dinner = calories * 0.25

    labels = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    values = [breakfast, lunch, snacks, dinner]

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    st.pyplot(plt)

# ---------------- WEEKLY PLANNER ----------------
with tab3:
    if st.button("Generate Weekly Plan"):
        if api_key:
            prompt = f"""
            Create a 7-day Indian meal plan table format.
            Calories Target: {round(calories)}
            Preferences: {food_pref}
            Restrictions: {diet_restrict}
            """

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            st.write(response.text)

# ---------------- HISTORY ----------------
with tab4:
    st.subheader("Previous Meal Plans")

    history = users[st.session_state.username]["history"]
    if history:
        for i, item in enumerate(history):
            st.write(f"### Plan {i+1}")
            st.write(item)
    else:
        st.info("No history available.")

# ---------------- LOGOUT ----------------
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()