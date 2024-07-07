import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import requests
import streamlit_app

class TestStreamlitApp(unittest.TestCase):
    def setUp(self):
        # Ensure Streamlit's session state is reset for each test
        st.session_state.clear()

    @patch('requests.post')
    def test_analyze_button(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [1]
        mock_post.return_value = mock_response

        st.session_state.text_input = "This is a test text"
        streamlit_app.st.button("Analyser")

        self.assertEqual(st.session_state.sentiment, "positif")
        self.assertTrue(mock_post.called)

    @patch('requests.post')
    def test_feedback_button(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        st.session_state.text_input = "This is a test text"
        st.session_state.sentiment = "positif"
        streamlit_app.st.button("Non")

        feedback_data = {
            "text": "This is a test text",
            "predicted_sentiment": "positif",
            "feedback": "Non"
        }
        mock_post.assert_called_with(
            "https://api-projet-7.azurewebsites.net/feedback",
            json=feedback_data,
            headers={"Content-Type": "application/json"},
        )
        self.assertTrue(st.session_state.feedback_given)

if __name__ == '__main__':
    unittest.main()
