import json
from model.comment import Comment

class Item:

    def __init__(self, json_str_or_dict = None):
        if json_str_or_dict is not None :
            if isinstance(json_str_or_dict, dict):
                self.__dict__ = json_str_or_dict
            else:
                self.__dict__ = json.loads(json_str_or_dict)

            #deep conversion
            for i in range(len(self.comments)):
                self.comments[i] = Comment(self.comments[i])
        else:
            self.name = ""
            self.url = ""
            self.description = ""
            self.comments = []
            self.error = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def __str__(self):
        return self.toJson()

    def fromJson(str) :
        return Item(str)

    def is_same(self, other) :
        return self.url == other.url

class ItemEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)