class User:
    _next_id = 1

    def __init__(self, name: str):
        self.id = User._next_id
        User._next_id += 1
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("ID должен быть положительным целым числом.")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя пользователя должно быть непустой строкой.")
        self._name = value.strip()