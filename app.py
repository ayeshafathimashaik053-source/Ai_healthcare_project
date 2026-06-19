import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("🩺 AI Health Risk & Suggestion System")
st.caption("🤖 Model: Random Forest Classifier")

st.warning("⚠️ This system provides suggestions only and is not a medical diagnosis.")

# ---------------- INPUT ----------------

age = st.slider("Age", 1, 100)
gender = st.selectbox("Gender", ["Male", "Female"])
severity = st.selectbox("Symptom Severity", ["Mild", "Moderate", "Severe"])
duration = st.selectbox("Duration of Symptoms", ["1-2 days", "3-5 days", "More than 5 days"])

# ---------------- SYMPTOMS ----------------

symptoms_list = [
    "fever", "cough", "headache", "fatigue",
    "chest_pain", "breathlessness",
    "high_fever", "body_pain",
    "itching", "skin_rash",
    "yellowing_of_eyes", "yellowish_skin",
    "vomiting", "dizziness",
    "nausea", "loss_of_appetite",
    "sweating", "chills",
    "abdominal_pain", "runny_nose"
]

selected_symptoms = st.multiselect("Select Your Symptoms", symptoms_list)

# ---------------- INPUT VECTOR ----------------

input_data = np.zeros((1, len(symptoms_list)))

for symptom in selected_symptoms:
    if symptom in symptoms_list:
        input_data[0][symptoms_list.index(symptom)] = 1

# ---------------- PREDICT ----------------

if st.button("Predict"):

    prediction = model.predict(input_data)[0]

    # Risk logic
    count = len(selected_symptoms)

    if count >= 6:
        risk = "High 🔴"
    elif count >= 3:
        risk = "Medium 🟡"
    else:
        risk = "Low 🟢"

    # Rule-based correction
    if "yellowing_of_eyes" in selected_symptoms or "yellowish_skin" in selected_symptoms:
        prediction = "Jaundice"
        risk = "High 🔴"

    elif "chest_pain" in selected_symptoms and "breathlessness" in selected_symptoms:
        prediction = "Heart Issue"
        risk = "High 🔴"

    elif "high_fever" in selected_symptoms and "body_pain" in selected_symptoms:
        prediction = "Viral Fever"

    elif "itching" in selected_symptoms and "skin_rash" in selected_symptoms:
        prediction = "Skin Allergy"

    elif "vomiting" in selected_symptoms and "nausea" in selected_symptoms:
        prediction = "Food Poisoning"

    elif "runny_nose" in selected_symptoms and "cough" in selected_symptoms:
        prediction = "Common Cold"

    # Recommendations
    if "Heart" in prediction:
        recommendation = "⚠️ Seek immediate medical attention"

    elif "Jaundice" in prediction:
        recommendation = "Avoid oily food, consult doctor"

    elif "Fever" in prediction:
        recommendation = "Take rest, drink fluids"

    else:
        recommendation = "Consult doctor if symptoms persist"

    # Output
    st.subheader("🩺 Possible Condition:")
    st.success(prediction)

    st.subheader("⚠️ Risk Level:")
    st.warning(risk)

    st.subheader("💡 Recommendation:")
    st.info(recommendation)