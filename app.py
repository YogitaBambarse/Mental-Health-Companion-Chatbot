import streamlit as st
from PIL import Image
import google.generativeai as genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from dotenv import load_dotenv
import tempfile
import os

# ---------------- ENV CONFIG ----------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Health Companion", layout="wide")

# ---------------- GLASS UI CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}
.glass-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.2);
}
.stButton>button {
    background: linear-gradient(45deg, #ff6ec4, #7873f5);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🤖 AI Health Companion</h1>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("👤 User Profile")

weight = st.sidebar.number_input("Weight (kg)", 30, 150, 60)
height = st.sidebar.number_input("Height (cm)", 120, 210, 165)
age = st.sidebar.number_input("Age", 10, 80, 22)

medical = st.sidebar.text_area("Medical Conditions", "None")
fitness = st.sidebar.text_area("Fitness Routine", "30 min workout daily")
food_pref = st.sidebar.text_area("Food Preferences", "Veg")
diet_restrict = st.sidebar.text_area("Dietary Restrictions", "None")

# ---------------- BMI ----------------
bmi = weight / ((height/100)**2)

if bmi < 18.5:
    category = "Underweight"
elif 18.5 <= bmi < 24.9:
    category = "Normal"
elif 25 <= bmi < 29.9:
    category = "Overweight"
else:
    category = "Obese"

st.sidebar.success(f"BMI: {round(bmi,2)} ({category})")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["🍽 Meal Plan", "📸 Food Analysis", "📊 Insights"])

# ---------------- MEAL PLAN ----------------
peal Plan")

    if api_key:
        if st.button("Generate AI Meal Plan 🍽"):
            with st.spinner("Generating your smart meal plan..."):

                prompt = f"""
                Create a detailed one-day Indian meal plan.
                User details:
                Age: {age}
                Weight: {weight} kg
                Height: {height} cm
                BMI: {round(bmi,2)} ({category})
                Medical Conditions: {medical}
                Food Preferences: {food_pref}
                Dietary Restrictions: {diet_restrict}
                Daily Calories Target: {round(calories)} kcal

                Provide:
                - Breakfast
                - Lunch
                - Snacks
                - Dinner
                - Approximate calories per meal
                - Health tips
                """

                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)

                st.success("Meal Plan Generated Successfully ✅")
                st.write(response.text)

                # Store for PDF
                st.session_state["meal_plan"] = response.text
    else:
        st.error("API Key not configured.")

    st.markdown("</div>", unsafe_allow_html=True)
# ---------------- FOOD ANALYSIS ----------------
with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Upload Food Image")
    uploaded_file = st.file_uploader("Choose Image", type=["jpg","jpeg","png"])

    analysis_text = ""

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

        if api_key:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                ["Analyze this food image and provide calories, protein, carbs and fats.", image]
            )
            analysis_text = response.text
            st.success("AI Analysis Complete ✅")
            st.write(analysis_text)
        else:
            st.error("API Key not found. Add GEMINI_API_KEY in Streamlit Secrets.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INSIGHTS ----------------
with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Health Overview")
    st.write(f"Age: {age}")
    st.write(f"Medical Condition: {medical}")
    st.write(f"Fitness Routine: {fitness}")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PDF REPORT ----------------
if st.button("📄 Download Health Report"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI Health Report", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"BMI: {round(bmi,2)} ({category})", styles['Normal']))
    elements.append(Paragraph(f"Daily Calories: {round(calories)} kcal", styles['Normal']))
    elements.append(Paragraph(f"Medical Conditions: {medical}", styles['Normal']))

    doc.build(elements)

    with open(temp_file.name, "rb") as f:
        st.download_button("Download PDF", f, file_name="Health_Report.pdf")

    os.unlink(temp_file.name)
