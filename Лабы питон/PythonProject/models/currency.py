class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int, id: int = None):
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
    def id(self, val):
        self._id = val

    @property
    def num_code(self):
        return self._num_code

    @num_code.setter
    def num_code(self, val: str):
        if not (isinstance(val, str) and len(val) == 3 and val.isdigit()):
            raise ValueError("NumCode должен быть строкой из 3 цифр")
        self._num_code = val

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, val: str):
        if not (isinstance(val, str) and len(val) == 3):
            raise ValueError("CharCode должен быть строкой из 3 букв")
        self._char_code = val.upper()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val: str):
        if not (isinstance(val, str) and val.strip()):
            raise ValueError("Название валюты не может быть пустым")
        self._name = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: float):
        if not isinstance(val, (int, float)) or val <= 0:
            raise ValueError("Курс должен быть положительным числом")
        self._value = float(val)

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, val: int):
        if not isinstance(val, int) or val <= 0:
            raise ValueError("Номинал должен быть положительным целым числом")
        self._nominal = val