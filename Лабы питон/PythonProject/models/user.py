class User:
    def __init__(self, name: str, id: int = None):
        self.id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val: str):
        if not (isinstance(val, str) and val.strip()):
            raise ValueError("Имя пользователя должно быть непустой строкой")
        self._name = val.strip()


