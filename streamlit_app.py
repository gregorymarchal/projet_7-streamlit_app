import streamlit as st
import requests
import time

# Streamlit application title
st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

# Text area for user input
text_input = st.text_area("Entrez le texte (en anglais) dont vous souhaitez analyser le sentiment :")

# Initialize session state
if "sentiment" not in st.session_state:
    st.session_state.sentiment = None

# Analyze button
if st.button("Analyser"):
    if text_input:
        # Replace the URL with your Flask backend on Azure
        url = "https://api-projet-7.azurewebsites.net/predict"
        response = requests.post(
            url,
            json={"text": text_input},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        predicted_class_id = result[0]
        st.session_state.sentiment = "positif" if predicted_class_id == 1 else "négatif"
        st.write(f"Le sentiment prédit est : *{st.session_state.sentiment}*.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")

# Feedback section
if st.session_state.sentiment:
    st.write("Le sentiment prédit était-il correct ?")
    if st.button("Oui"):
        st.write("Merci pour votre retour !")
        time.sleep(2)  # Pause for 2 seconds
        st.experimental_rerun()
    if st.button("Non"):
        feedback_data = {
            "text": text_input,
            "predicted_sentiment": st.session_state.sentiment,
            "feedback": "Non"
        }
        # Send feedback to Flask backend
        feedback_url = "https://api-projet-7.azurewebsites.net/feedback"
        feedback_response = requests.post(
            feedback_url,
            json=feedback_data,
            headers={"Content-Type": "application/json"},
        )
        st.write("Merci pour votre retour !")
        time.sleep(2)  # Pause for 2 seconds
        st.experimental_rerun()
