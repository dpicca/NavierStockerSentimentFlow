import unittest
from SentimentFlow.plotting import normalize_data

class TestPlotting(unittest.TestCase):
    def test_normalize_data(self):
        data = [1, 2, 3, 4, 5]
        normalized = normalize_data(data)
        self.assertEqual(len(normalized), len(data))
        self.assertTrue(all(-1 <= x <= 1 for x in normalized))

if __name__ == '__main__':
    unittest.main()
