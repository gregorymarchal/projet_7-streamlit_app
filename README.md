# Sentiment Analysis Project

This project is a Streamlit web application for sentiment analysis using Deep Learning. The application allows users to input text and receive a sentiment analysis (positive or negative) using a backend FastAPI service hosted on Azure.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Logging](#logging)
- [Feedback](#feedback)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/gregorymarchal/projet_7-streamlit_app.git
    cd projet_7-streamlit_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter the text you want to analyze in the text area and click "Analyser".

## Testing

Unit tests are provided to ensure the functionality of the sentiment analysis.

1. Run the tests using:
    ```sh
    python -m unittest discover
    ```

The test cases are defined in `test_app.py` and use the `unittest` framework with `unittest.mock` for mocking API responses.

## Logging

This application uses Azure Application Insights for logging user feedback. Ensure you have set up the correct connection string for Azure Application Insights in the `app.py` file.

## Feedback

If the sentiment prediction is incorrect, users can provide feedback directly in the application. This feedback is logged in Azure Application Insights for further analysis and model improvement.
