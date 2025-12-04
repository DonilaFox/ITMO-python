import logging
import io
from logger import logger
from get_currency import get_currencies

# === 1. Логирование в stdout ===
print("=== Логирование в stdout ===")
@logger()
def get_usd():
    return get_currencies(["USD"])

try:
    result = get_usd()
    print("Результат:", result)
except Exception as e:
    print("Ошибка:", e)

# === 2. Логирование в StringIO ===
print("\n=== Логирование в StringIO ===")
stream = io.StringIO()

@logger(handle=stream)
def get_eur():
    return get_currencies(["EUR"])

try:
    result = get_eur()
    print("Результат:", result)
    print("Лог из StringIO:")
    print(stream.getvalue())
except Exception as e:
    print("Ошибка:", e)

# === 3. Логирование в файл через logging ===
print("\n=== Логирование в файл currency.log ===")
file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

if not file_logger.handlers:
    handler = logging.FileHandler("currency.log", encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    file_logger.addHandler(handler)

@logger(handle=file_logger)
def get_usd_eur():
    return get_currencies(["USD", "EUR"])

try:
    result = get_usd_eur()
    print("Результат:", result)
except Exception as e:
    print("Ошибка:", e)

print("\n Все логи записаны в файлы.")