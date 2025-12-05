class Currency:
    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise TypeError("ID валюты должен быть строкой.")
        self._id = value

    @property
    def num_code(self):
        return self._num_code

    @num_code.setter
    def num_code(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 3):
            raise ValueError("Цифровой код должен быть строкой из 3 цифр.")
        self._num_code = value

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, value):
        if not (isinstance(value, str) and len(value) == 3):
            raise ValueError("Символьный код должен быть строкой из 3 букв.")
        self._char_code = value.upper()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название валюты должно быть непустой строкой.")
        self._name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Курс должен быть числом.")
        if value <= 0:
            raise ValueError("Курс должен быть положительным.")
        self._value = float(value)

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Номинал должен быть положительным целым числом.")
        self._nominal = value