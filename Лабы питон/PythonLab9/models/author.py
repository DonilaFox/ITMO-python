class Author:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя автора должно быть непустой строкой.")
        self._name = value.strip()

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Группа должна быть непустой строкой.")
        self._group = value.strip()