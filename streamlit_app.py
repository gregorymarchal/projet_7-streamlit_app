import os
import streamlit as st
import requests

api_url = os.getenv('API_URL')

# Streamlit application title
st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

# Initialize session state
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "sentiment" not in st.session_state:
    st.session_state.sentiment = None
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

# Text area for user input
st.session_state.text_input = st.text_area("Entrez le texte (en anglais) dont vous souhaitez analyser le sentiment :", st.session_state.text_input)

# Analyze button
if st.button("Analyser"):
    if st.session_state.text_input:
        # Replace the URL with your Flask backend on Azure
        predict_url = f"{api_url}/predict"
        predict_response = requests.post(
            predict_url,
            json={"text": st.session_state.text_input},
            headers={"Content-Type": "application/json"},
        )
        predict_response.raise_for_status()  # Raise an exception for HTTP errors
        result = predict_response.json()
        predicted_class_id = result[0]
        st.session_state.sentiment = "positif" if predicted_class_id == 1 else "négatif"
        st.write(f"Le sentiment prédit est : *{st.session_state.sentiment}*.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")

# Feedback section
if st.session_state.sentiment and not st.session_state.feedback_given:
    st.write("Le sentiment prédit était-il correct ?")
    if st.button("Oui"):
        st.session_state.feedback_given = True
    if st.button("Non"):
        feedback_data = {
            "text": st.session_state.text_input,
            "predicted_sentiment": st.session_state.sentiment,
            "feedback": "Non"
        }
        # Send feedback to Flask backend
        feedback_url = f"{api_url}/feedback"
        feedback_response = requests.post(
            feedback_url,
            json=feedback_data,
            headers={"Content-Type": "application/json"},
        )
        st.session_state.feedback_given = True

# Show feedback acknowledgment if feedback was given
if st.session_state.feedback_given:
    st.write("Merci pour votre retour !")
    if st.button("Faire une nouvelle prédiction"):
        st.session_state.text_input = ""
        st.session_state.sentiment = None
        st.session_state.feedback_given = False
        st.rerun()
