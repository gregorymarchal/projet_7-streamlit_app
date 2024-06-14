import streamlit as st
import requests

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
            predicted_class_id = result['predicted_class_id']
            sentiment = "positif" if predicted_class_id == 1 else "négatif"
            st.write(f"Le sentiment prédit est : {sentiment}")
        else:
            st.write("Erreur dans la requête.")
    else:
        st.write("Entrez s'il-vous-plaît le texte dont vous souhaitez analyser le sentiment.")
