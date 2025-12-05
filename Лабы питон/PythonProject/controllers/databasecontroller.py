import sqlite3
import urllib.request
import xml.etree.ElementTree as ET
from models.currency import Currency
from models.user import User

class CurrencyRatesCRUD:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._load_initial_data()

    def _create_tables(self):
        # Валюты
        self.conn.execute('''
            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL CHECK(length(num_code) = 3),
                char_code TEXT NOT NULL CHECK(length(char_code) = 3),
                name TEXT NOT NULL,
                value REAL NOT NULL CHECK(value > 0),
                nominal INTEGER NOT NULL CHECK(nominal > 0)
            )
        ''')
        # Пользователи
        self.conn.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        # Подписки (связь многие-ко-многим)
        self.conn.execute('''
            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def _load_initial_data(self):
        url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        currencies_added = 0
        try:
            with urllib.request.urlopen(url) as response:
                xml_data = response.read()
            root = ET.fromstring(xml_data)
            for valute in root.findall('Valute'):
                num_code = valute.find('NumCode').text
                char_code = valute.find('CharCode').text
                name = valute.find('Name').text
                nominal = int(valute.find('Nominal').text)
                value_str = valute.find('Value').text.replace(',', '.')
                value = float(value_str)

                self.create_currency(Currency(num_code, char_code, name, value, nominal))
                currencies_added += 1
        except Exception as e:
            print(f"Ошибка загрузки из ЦБ: {e}. Используем резервные данные.")
            fallback = [
                ("840", "USD", "Доллар США", 78.84, 1),
                ("978", "EUR", "Евро", 91.73, 1),
                ("156", "CNY", "Юань", 11.02, 1),
                ("036", "AUD", "Австралийский доллар", 51.37, 1),
                ("826", "GBP", "Фунт стерлингов", 104.83, 1),
            ]
            for num, char, name, val, nom in fallback:
                self.create_currency(Currency(num, char, name, val, nom))
            currencies_added = len(fallback)

        # Создание пользователей
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user (name) VALUES (?)", ("Alexander Radulov",))
        cur.execute("INSERT INTO user (name) VALUES (?)", ("Alexander Yelesin",))
        self.conn.commit()

        # Получаем ID пользователей
        user_ids = {}
        cur.execute("SELECT id, name FROM user")
        for row in cur.fetchall():
            user_ids[row['name']] = row['id']

        # Получаем ID валют
        currency_ids = {}
        cur.execute("SELECT id, char_code FROM currency")
        for row in cur.fetchall():
            currency_ids[row['char_code']] = row['id']

        # Подписки: Алексей → USD, EUR; Мария → CNY
        if 'Алексей' in user_ids and 'USD' in currency_ids:
            cur.execute("INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)",
                        (user_ids['Алексей'], currency_ids['USD']))
        if 'Алексей' in user_ids and 'EUR' in currency_ids:
            cur.execute("INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)",
                        (user_ids['Алексей'], currency_ids['EUR']))
        if 'Мария' in user_ids and 'CNY' in currency_ids:
            cur.execute("INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)",
                        (user_ids['Мария'], currency_ids['CNY']))

        self.conn.commit()
        print(f"Загружено {currencies_added} валют и 2 пользователя.")

    # === CRUD: CREATE ===
    def create_currency(self, currency: Currency):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO currency (num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            currency.num_code,
            currency.char_code,
            currency.name,
            currency.value,
            currency.nominal
        ))
        currency.id = cursor.lastrowid
        self.conn.commit()
        return currency

    # === CRUD: READ ===
    def read_all_currencies(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM currency")
        return [
            Currency(
                id=row['id'],
                num_code=row['num_code'],
                char_code=row['char_code'],
                name=row['name'],
                value=row['value'],
                nominal=row['nominal']
            )
            for row in cursor.fetchall()
        ]

    # === CRUD: UPDATE ===
    def update_currency_value(self, char_code: str, new_value: float):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE char_code = ?", (new_value, char_code.upper()))
        self.conn.commit()
        return cursor.rowcount > 0

    # === CRUD: DELETE ===
    def delete_currency(self, currency_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    # === Работа с пользователями ===
    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user")
        return [User(id=row['id'], name=row['name']) for row in cursor.fetchall()]

    def get_user_by_id(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return User(id=row['id'], name=row['name']) if row else None

    def get_user_currencies(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        ''', (user_id,))
        return [
            Currency(
                id=row['id'],
                num_code=row['num_code'],
                char_code=row['char_code'],
                name=row['name'],
                value=row['value'],
                nominal=row['nominal']
            )
            for row in cursor.fetchall()
        ]

    def close(self):
        self.conn.close()