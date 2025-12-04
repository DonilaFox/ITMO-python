import requests
from logger import logger

def get_currencies(currency_codes: list, url="https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют с API ЦБ РФ.
    Возвращает словарь вида: {"USD": 93.25, "EUR": 101.7}
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Не удаётся подключиться к API: {e}")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError(f"Некорректный JSON: {e}")

    if "Valute" not in data:
        raise KeyError("Ответ не содержит ключа 'Valute'")

    valute = data["Valute"]
    result = {}
    for code in currency_codes:
        if code not in valute:
            raise KeyError(f"Валюта {code} отсутствует в данных")
        currency_info = valute[code]
        if "Value" not in currency_info:
            raise KeyError(f"Для валюты {code} отсутствует значение 'Value'")
        value = currency_info["Value"]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты {code} имеет неверный тип: {type(value)}")
        result[code] = float(value)
    return result