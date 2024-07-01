import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Set up logging to Azure Application Insights
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=55f8c386-676e-4155-b920-c470270eb854'))

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

            st.write("Le sentiment prédit était-il correct ?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Oui"):
                    st.experimental_rerun()
            with col2:
                if st.button("Non"):
                    feedback_data = {
                        "text": text_input,
                        "predicted_sentiment": sentiment,
                        "feedback": "Non"
                    }
                    # Send feedback to Azure Application Insights
                    logger.info("User feedback", extra=feedback_data)
                    st.write("Merci pour votre retour !")
                    st.experimental_rerun()
        else:
            st.write("Erreur dans la requête.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")
