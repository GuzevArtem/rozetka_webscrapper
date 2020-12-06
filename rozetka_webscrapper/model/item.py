import json

class Item:
    def __init__(self):
        self.name = ""
        self.url = ""
        self.comments = []
        self.error = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

    def __str__(self):
        return self.toJson()

class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)