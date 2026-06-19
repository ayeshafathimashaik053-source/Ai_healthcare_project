import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Load dataset
df = pd.read_csv("dataset.csv")
df.rename(columns={"Disease": "disease"}, inplace=True)

# Extract symptoms
symptoms = set()
for col in df.columns[1:]:
    symptoms.update(df[col].dropna().unique())

symptoms = sorted(list(symptoms))

# ---------------- UI ----------------

st.title("🩺 AI Health Risk & Suggestion System")

st.write("⚠️ This system provides suggestions only and is not a medical diagnosis.")

st.subheader("👤 Enter Your Details")

age = st.slider("Age", 1, 100, 25)
gender = st.selectbox("Gender", ["Male", "Female"])

severity = st.selectbox("Symptom Severity", ["Mild", "Moderate", "Severe"])
duration = st.selectbox("Duration of Symptoms", ["1-2 days", "3-5 days", "More than 5 days"])

st.subheader("🤒 Select Your Symptoms")

selected_symptoms = []

for symptom in symptoms:
    if st.checkbox(symptom):
        selected_symptoms.append(symptom)

if selected_symptoms:
    st.write("Selected Symptoms:", selected_symptoms)

# ---------------- Prediction ----------------

if st.button("Predict"):

    # Create input vector
    input_vector = [0] * len(symptoms)

    for symptom in selected_symptoms:
        index = symptoms.index(symptom)
        input_vector[index] = 1

    input_array = np.array([input_vector])

    prediction = model.predict(input_array)[0]

    # ---------------- Risk Logic ----------------

    risk = "Low 🟢"

    if severity == "Moderate" or duration == "3-5 days":
        risk = "Medium 🟡"

    if severity == "Severe" or duration == "More than 5 days":
        risk = "High 🔴"

    # ---------------- Suggestions ----------------

    suggestions = {
        "Fungal infection": "Keep skin clean and dry. Use antifungal cream.",
        "Allergy": "Avoid allergens. Take antihistamines.",
        "Cold": "Take rest and drink warm fluids.",
        "Flu": "Take rest, fluids, and paracetamol.",
        "Acne": "Maintain hygiene and avoid oily foods.",
        "Migraine": "Avoid stress and take proper sleep.",
        "Heart Disease": "Consult a doctor immediately.",
        "Asthma": "Use inhaler and avoid dust.",
        "Dengue": "Consult doctor and stay hydrated.",
        "Malaria": "Seek medical treatment immediately."
    }

    recommendation = suggestions.get(prediction, "Consult a doctor for proper diagnosis.")

    # ---------------- Output ----------------

    st.success(f"🩺 Possible Condition: {prediction}")
    st.warning(f"⚠️ Risk Level: {risk}")
    st.info(f"💡 Recommendation: {recommendation}")