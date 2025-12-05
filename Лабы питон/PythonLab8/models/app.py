from .author import Author

class App:
    def __init__(self, name: str, version: str, author: Author):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название приложения должно быть строкой.")
        self._name = value.strip()

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Версия должна быть строкой.")
        self._version = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть объектом класса Author.")
        self._author = value