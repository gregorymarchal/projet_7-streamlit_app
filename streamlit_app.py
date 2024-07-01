import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

connection_string = "InstrumentationKey=55f8c386-676e-4155-b920-c470270eb854;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/;ApplicationId=499673b2-6e2a-4c76-a53c-2ad71070f331"

# Set up logging to Azure Application Insights
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Ensure all messages are captured
handler = AzureLogHandler(connection_string=connection_string)
logger.addHandler(handler)

logger.debug("Logger initialized and handler added.")

st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

text_input = st.text_area("Entrez le texte dont vous souhaitez analyser le sentiment :")

if st.button("Analyser"):
    logger.debug(f"Analyze button clicked with input: {text_input}")
    if text_input:
        # Remplacer l'URL par celle de votre backend FastAPI Azure
        url = "https://api-projet-7.azurewebsites.net/predict"
        response = requests.post(
            url,
            json={"text": text_input},
            headers={"Content-Type": "application/json"},
        )
        logger.debug(f"Request sent to {url} with status code {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            predicted_class_id = result[0]
            sentiment = "positif" if predicted_class_id == 1 else "négatif"
            st.write(f"Le sentiment prédit est : *{sentiment}*.")

            st.write("Le sentiment prédit était-il correct ?")
            if st.button("Oui"):
                logger.debug("Feedback 'Oui' clicked")
                st.experimental_rerun()
            elif st.button("Non"):
                feedback_data = {
                    "text": text_input,
                    "predicted_sentiment": sentiment,
                    "feedback": "Non"
                }
                # Send feedback to Azure Application Insights
                logger.warning("User feedback", extra=feedback_data)
                st.write("Merci pour votre retour !")
                st.experimental_rerun()
        else:
            st.write("Erreur dans la requête.")
            logger.error(f"Request failed with status code: {response.status_code} and response: {response.text}")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")
        logger.debug("No text input provided for analysis.")

# Ensure feedback handling is separate and persistent between runs
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

if st.session_state.feedback:
    st.write("Merci pour votre retour !")
    st.session_state.feedback = None
