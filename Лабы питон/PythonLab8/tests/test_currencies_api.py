import unittest
from utils.currencies_api import get_currencies

class TestCurrenciesAPI(unittest.TestCase):
    def test_get_currencies(self):
        currencies = get_currencies()
        self.assertGreater(len(currencies), 0)
        self.assertTrue(hasattr(currencies[0], 'char_code'))

if __name__ == '__main__':
    unittest.main()