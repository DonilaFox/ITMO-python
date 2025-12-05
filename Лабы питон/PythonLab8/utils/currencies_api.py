import xml.etree.ElementTree as ET
import urllib.request
from models.currency import Currency

def get_currencies() -> list[Currency]:
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)

        currencies = []
        for valute in root.findall('Valute'):
            id_attr = valute.attrib['ID']
            num_code = valute.find('NumCode').text
            char_code = valute.find('CharCode').text
            nominal = int(valute.find('Nominal').text)
            name = valute.find('Name').text
            value_str = valute.find('Value').text.replace(',', '.')
            value = float(value_str)

            currency = Currency(
                id=id_attr,
                num_code=num_code,
                char_code=char_code,
                name=name,
                value=value,
                nominal=nominal
            )
            currencies.append(currency)
        return currencies
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении курсов: {e}")