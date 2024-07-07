import streamlit as st
import requests

# Streamlit application title
st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

# Text area for user input
text_input = st.text_area("Entrez le texte dont vous souhaitez analyser le sentiment :")

# Analyze button
if st.button("Analyser"):
    if text_input:
        try:
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
            sentiment = "positif" if predicted_class_id == 1 else "négatif"
            st.write(f"Le sentiment prédit est : *{sentiment}*.")
        except requests.RequestException as e:
            st.write(f"Erreur dans la requête: {e}")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")

# Feedback section (separated from the analysis button to avoid nested buttons)
if "sentiment" in locals() and sentiment:
    st.write("Le sentiment prédit était-il correct ?")
    if st.button("Non"):
        feedback_data = {
            "text": text_input,
            "predicted_sentiment": sentiment,
            "feedback": "Non"
        }
        try:
            # Send feedback to Flask backend
            feedback_url = "https://api-projet-7.azurewebsites.net/feedback"
            feedback_response = requests.post(
                feedback_url,
                json=feedback_data,
                headers={"Content-Type": "application/json"},
            )
            feedback_response.raise_for_status()  # Raise an exception for HTTP errors
            st.write("Merci pour votre retour !")
        except requests.RequestException as e:
            st.write(f"Erreur dans l'envoi du feedback: {e}")
