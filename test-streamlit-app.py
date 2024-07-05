import unittest
from unittest.mock import patch
from app import analyze_sentiment

class TestSentimentAnalysis(unittest.TestCase):

    @patch('app.requests.post')
    def test_analyze_sentiment_positive(self, mock_post):
        # Mocking the API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [1]

        sentiment = analyze_sentiment("This is a good product!")
        self.assertEqual(sentiment, "positif")

    @patch('app.requests.post')
    def test_analyze_sentiment_negative(self, mock_post):
        # Mocking the API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [0]

        sentiment = analyze_sentiment("This is a bad product!")
        self.assertEqual(sentiment, "négatif")

    @patch('app.requests.post')
    def test_analyze_sentiment_error(self, mock_post):
        # Mocking the API response with an error
        mock_post.return_value.status_code = 500

        with self.assertRaises(Exception) as context:
            analyze_sentiment("This is a test.")
        
        self.assertTrue("Erreur dans la requête." in str(context.exception))

if __name__ == '__main__':
    unittest.main()
