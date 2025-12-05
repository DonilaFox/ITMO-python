import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController
from models.currency import Currency

class TestCurrencyController(unittest.TestCase):

    def test_list_currencies_returns_currency_objects(self):
        # Arrange
        mock_db = MagicMock()
        mock_currency = Currency("840", "USD", "Доллар США", 78.84, 1, id=1)
        mock_db.read_all_currencies.return_value = [mock_currency]

        controller = CurrencyController(mock_db)

        # Act
        result = controller.list_currencies()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Currency)
        self.assertEqual(result[0].char_code, "USD")
        self.assertEqual(result[0].value, 78.84)
        mock_db.read_all_currencies.assert_called_once()

    def test_update_currency_calls_db_with_correct_args(self):
        # Arrange
        mock_db = MagicMock()
        mock_db.update_currency_value.return_value = True
        controller = CurrencyController(mock_db)

        # Act
        success = controller.update_currency("EUR", 95.5)

        # Assert
        self.assertTrue(success)
        mock_db.update_currency_value.assert_called_once_with("EUR", 95.5)

    def test_delete_currency_calls_db_with_correct_id(self):
        # Arrange
        mock_db = MagicMock()
        mock_db.delete_currency.return_value = True
        controller = CurrencyController(mock_db)

        # Act
        success = controller.delete_currency(5)

        # Assert
        self.assertTrue(success)
        mock_db.delete_currency.assert_called_once_with(5)

    def test_update_currency_handles_false_return(self):
        # Arrange
        mock_db = MagicMock()
        mock_db.update_currency_value.return_value = False  # валюта не найдена
        controller = CurrencyController(mock_db)

        # Act
        success = controller.update_currency("XYZ", 100.0)

        # Assert
        self.assertFalse(success)
        mock_db.update_currency_value.assert_called_once_with("XYZ", 100.0)

    def test_delete_currency_handles_nonexistent_id(self):
        # Arrange
        mock_db = MagicMock()
        mock_db.delete_currency.return_value = False
        controller = CurrencyController(mock_db)

        # Act
        success = controller.delete_currency(999)

        # Assert
        self.assertFalse(success)
        mock_db.delete_currency.assert_called_once_with(999)