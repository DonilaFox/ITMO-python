import unittest
from models.author import Author
from models.user import User
from models.currency import Currency

class TestModels(unittest.TestCase):
    def test_author_valid(self):
        a = Author("Alexander", "P3123")
        self.assertEqual(a.name, "Alexander")
        self.assertEqual(a.group, "P3123")

    def test_author_invalid_name(self):
        with self.assertRaises(ValueError):
            Author("", "P3123")

    def test_currency_valid(self):
        c = Currency("R01235", "840", "USD", "Доллар США", 75.5, 1)
        self.assertEqual(c.char_code, "USD")
        self.assertEqual(c.value, 75.5)

    def test_currency_invalid_char_code(self):
        with self.assertRaises(ValueError):
            Currency("R0", "840", "US", "Доллар", 75.5, 1)

if __name__ == '__main__':
    unittest.main()