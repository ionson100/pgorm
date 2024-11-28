import json


class JsonTest:
    id: int
    name: str

    def __init__(self):
        self.id = 234
        self.name = 'test'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)