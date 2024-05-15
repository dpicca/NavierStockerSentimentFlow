import unittest
import numpy as np

from SentimentFlow.sentiment_analysis import _calculate_sentiment_density, calculate_sentiment_pressure, calculate_sentiment_viscosity, calculate_external_contextual_force
class TestSentimentAnalysis(unittest.TestCase):
    def test_calculate_sentiment_density(self):
        scores = [0.1, 0.2, 0.3, 0.4]
        density = _calculate_sentiment_density(scores)
        self.assertAlmostEqual(density, 1.0)

    def test_calculate_sentiment_pressure(self):
        score = 0.5
        keywords = ["happy", "joyful"]
        text = "This is a very happy day."
        pressure = calculate_sentiment_pressure(score, keywords, text)
        self.assertAlmostEqual(pressure, 0.5)

    def test_calculate_sentiment_viscosity(self):
        scores = [0.1, 0.2, 0.3, 0.4]
        viscosity = calculate_sentiment_viscosity(scores)
        self.assertAlmostEqual(viscosity, 0.129099)

    def test_calculate_external_contextual_force(self):
        polarity = 0.75
        force = calculate_external_contextual_force(polarity)
        self.assertAlmostEqual(force, 0.75)

if __name__ == '__main__':
    unittest.main()
