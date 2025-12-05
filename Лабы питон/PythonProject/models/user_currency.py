class UserCurrency:
    def __init__(self, user_id: int, currency_id: int, id: int = None):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, val: int):
        if not (isinstance(val, int) and val > 0):
            raise ValueError("user_id должен быть положительным целым числом")
        self._user_id = val

    @property
    def currency_id(self):
        return self._currency_id

    @currency_id.setter
    def currency_id(self, val: int):
        if not (isinstance(val, int) and val > 0):
            raise ValueError("currency_id должен быть положительным целым числом")
        self._currency_id = val