import streamlit as st
import requests

st.title("Text Classification with Hugging Face Model")

text_input = st.text_area("Enter text for classification:")

if st.button("Classify"):
    if text_input:
        # Replace the URL with your Azure FastAPI backend URL
        url = "https://api-projet-7.azurewebsites.net/predict"
        response = requests.post(
            url,
            json={"text": text_input},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            result = response.json()
            st.write(f"Predicted Class ID: {result['predicted_class_id']}")
        else:
            st.write("Error in classification request")
    else:
        st.write("Please enter some text for classification")
