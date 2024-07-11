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
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. Set up the Flask backend URL environment variable:
    ```sh
    API_URL="<your_api_url>"
    ```

2. Run the Streamlit application:
    ```sh
    streamlit run streamlit_app.py
    ```

The application will be available at `http://localhost:8501`.

### Running Tests

To run the unit tests, use the following command:
```sh
python3 -m unittest test_streamlit_app.py
