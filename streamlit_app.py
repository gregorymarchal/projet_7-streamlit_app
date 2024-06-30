import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Set up logging to Azure Application Insights
logger = logging.getLogger(__name__)
connection_string = "InstrumentationKey=55f8c386-676e-4155-b920-c470270eb854;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/;ApplicationId=499673b2-6e2a-4c76-a53c-2ad71070f331"
logger.addHandler(AzureLogHandler(connection_string=connection_string))

st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

text_input = st.text_area("Entrez le texte dont vous souhaitez analyser le sentiment :")

if st.button("Analyser"):
    if text_input:
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
            st.write(f"Le sentiment prédit est : *{sentiment}*.")

            # Add feedback section
            feedback = st.radio("Le sentiment prédit était-il correct ?", ("Oui", "Non"))

            if feedback == "Non":
                feedback_data = {
                    "text": text_input,
                    "predicted_sentiment": sentiment,
                    "feedback": feedback
                }
                # Send feedback to Azure Application Insights
                logger.warning("User feedback", extra=feedback_data)
                st.write("Merci pour votre retour !")

        else:
            st.write("Erreur dans la requête.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")
