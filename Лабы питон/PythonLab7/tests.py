import unittest
import io
from unittest.mock import patch, Mock
import requests  # ← добавьте импорт requests!
from get_currency import get_currencies
from logger import logger


class TestGetCurrencies(unittest.TestCase):

    @patch("get_currency.requests.get")
    def test_valid_response(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.7}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.7})

    @patch("get_currency.requests.get")
    def test_connection_error(self, mock_get):
        # ✅ Используем настоящий requests.RequestException
        mock_get.side_effect = requests.RequestException("Network error")
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"])

    @patch("get_currency.requests.get")
    def test_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        with self.assertRaises(ValueError):
            get_currencies(["USD"])

    @patch("get_currency.requests.get")
    def test_missing_valute_key(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Other": "data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with self.assertRaises(KeyError):
            get_currencies(["USD"])

    @patch("get_currency.requests.get")
    def test_currency_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {"EUR": {"Value": 100}}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with self.assertRaises(KeyError):
            get_currencies(["USD"])

    @patch("get_currency.requests.get")
    def test_invalid_currency_type(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {"USD": {"Value": "ninety"}}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with self.assertRaises(TypeError):
            get_currencies(["USD"])


class TestLoggerDecorator(unittest.TestCase):

    def test_successful_execution(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def multiply(x, y):
            return x * y

        result = multiply(3, 4)
        self.assertEqual(result, 12)

        logs = stream.getvalue()
        self.assertIn("Вызов функции multiply с аргументами: (3, 4)", logs)
        self.assertIn("успешно завершена. Результат: 12", logs)

    def test_exception_raised(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def divide(x, y):
            return x / y

        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

        logs = stream.getvalue()
        self.assertIn("Исключение в функции divide: ZeroDivisionError", logs)


class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        self.wrapped = wrapped

    @patch("get_currency.requests.get")
    def test_logging_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Invalid URL")
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


if __name__ == '__main__':
    unittest.main()