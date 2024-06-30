import streamlit as st
import requests
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Set up logging to Azure Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=55f8c386-676e-4155-b920-c470270eb854'))

st.title("Projet 7 : Réalisez une analyse de sentiments grâce au Deep Learning")

# Function to reset the session state
def reset_session():
    st.session_state['analyze_button_clicked'] = False
    st.session_state['sentiment'] = ""
    st.session_state['feedback_given'] = False

# Initialize session state variables if they don't exist
if 'analyze_button_clicked' not in st.session_state:
    st.session_state['analyze_button_clicked'] = False
if 'sentiment' not in st.session_state:
    st.session_state['sentiment'] = ""
if 'feedback_given' not in st.session_state:
    st.session_state['feedback_given'] = False

text_input = st.text_area("Entrez le texte dont vous souhaitez analyser le sentiment :")

if st.button("Analyser"):
    if text_input:
        st.session_state['analyze_button_clicked'] = True
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
            st.session_state['sentiment'] = sentiment
        else:
            st.write("Erreur dans la requête.")
            st.session_state['analyze_button_clicked'] = False
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")

if st.session_state['analyze_button_clicked'] and not st.session_state['feedback_given']:
    feedback = st.radio("Le sentiment prédit était-il correct ?", ["Oui", "Non"], key='feedback_radio')
    
    if st.button("Soumettre le retour"):
        if feedback == "Oui":
            st.write("Merci pour votre retour !")
        elif feedback == "Non":
            feedback_data = {
                "text": text_input,
                "predicted_sentiment": st.session_state['sentiment'],
                "feedback": feedback
            }
            # Send feedback to Azure Application Insights
            logger.warning("User feedback", extra=feedback_data)
            st.write("Merci pour votre retour !")
        
        # Set feedback given to true to hide the feedback section
        st.session_state['feedback_given'] = True

# Reset session state after feedback submission
if st.session_state['feedback_given']:
    reset_session()
