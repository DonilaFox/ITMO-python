class UserCurrency:
    _next_id = 1

    def __init__(self, user_id: int, currency_id: str):
        self.id = UserCurrency._next_id
        UserCurrency._next_id += 1
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("ID должен быть положительным целым числом.")
        self._id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("user_id должен быть положительным целым числом.")
        self._user_id = value

    @property
    def currency_id(self):
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value):
        if not isinstance(value, str):
            raise TypeError("currency_id должен быть строкой.")
        self._currency_id = value