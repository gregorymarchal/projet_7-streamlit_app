import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Set up logging to Azure Application Insights
logger = logging.getLogger(__name__)
connection_string = "InstrumentationKey=55f8c386-676e-4155-b920-c470270eb854;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/;ApplicationId=499673b2-6e2a-4c76-a53c-2ad71070f331"
logger.addHandler(AzureLogHandler(connection_string=connection_string))

st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

# Initialize session state for feedback and sentiment
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'sentiment' not in st.session_state:
    st.session_state.sentiment = None
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""
if 'feedback_logged' not in st.session_state:
    st.session_state.feedback_logged = False

# Text input
text_input = st.text_area("Entrez le texte dont vous souhaitez analyser le sentiment :", st.session_state.text_input)

if st.button("Analyser"):
    if text_input:
        # Save the text input to session state
        st.session_state.text_input = text_input
        
        # Remplacer l'URL par celle de votre backend FastAPI Azure
        url = "https://api-projet-7.azurewebsites.net/predict"
        response = requests.post(
            url,
            json={"text": text_input},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            result = response.json()
            predicted_class_id = result[0]
            sentiment = "positif" if predicted_class_id == 1 else "négatif"
            st.session_state.sentiment = sentiment
            st.write(f"Le sentiment prédit est : *{sentiment}*.")

            # Reset feedback state
            st.session_state.feedback = None
            st.session_state.feedback_logged = False

        else:
            st.write("Erreur dans la requête.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")

# Show feedback section if sentiment is available
if st.session_state.sentiment:
    feedback = st.radio("Le sentiment prédit était-il correct ?", ("Oui", "Non"))

    if feedback != st.session_state.feedback:
        st.session_state.feedback = feedback
        st.session_state.feedback_logged = False

    if st.session_state.feedback == "Non" and not st.session_state.feedback_logged:
        feedback_data = {
            "text": st.session_state.text_input,
            "predicted_sentiment": st.session_state.sentiment,
            "feedback": st.session_state.feedback
        }
        # Send feedback to Azure Application Insights
        logger.warning("User feedback", extra=feedback_data)
        st.write("Merci pour votre retour !")
        st.session_state.feedback_logged = True

# Show the validate button if feedback is "Non"
if st.session_state.feedback == "Non" and st.session_state.feedback_logged:
    if st.button("Valider l'envoi de trace"):
        feedback_data = {
            "text": st.session_state.text_input,
            "predicted_sentiment": st.session_state.sentiment,
            "feedback": st.session_state.feedback
        }
        logger.warning("Trace validation button clicked", extra=feedback_data)
        st.write("Trace envoyée avec succès.")
        st.session_state.feedback_logged = False
