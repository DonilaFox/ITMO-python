from controllers.databasecontroller import CurrencyRatesCRUD

class CurrencyController:
    def __init__(self, db: CurrencyRatesCRUD):
        self.db = db

    def list_currencies(self):
        return self.db.read_all_currencies()

    def update_currency(self, char_code: str, new_value: float):
        return self.db.update_currency_value(char_code, new_value)

    def delete_currency(self, currency_id: int):
        return self.db.delete_currency(currency_id)