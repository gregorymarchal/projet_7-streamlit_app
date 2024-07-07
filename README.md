# Streamlit Sentiment Analysis Application

This project is a Streamlit application that allows users to analyze the sentiment of a given text using a pre-trained model hosted on a Flask backend. It also collects user feedback on the predictions.

## Setup

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Install Dependencies

1. Clone the repository:
    ```sh
    git clone https://github.com/gregorymarchal/projet_7-streamlit_app.git
    cd projet_7-streamlit_app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install streamlit
    ```

### Running the Application

1. Set up the Flask backend URL in `app.py`:
    ```python
    url = "https://api-projet-7.azurewebsites.net/predict"
    feedback_url = "https://api-projet-7.azurewebsites.net/feedback"
    ```

2. Run the Streamlit application:
    ```sh
    streamlit run streamlit_app.py
    ```

The application will be available at `http://localhost:8501`.

### Running Tests

To run the unit tests, use the following command:
```sh
python -m unittest test_streamlit_app.py
