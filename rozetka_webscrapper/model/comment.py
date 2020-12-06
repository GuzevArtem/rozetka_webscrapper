import json

class Comment:

    def __init__(self, json_str_or_dict = None):
        if json_str_or_dict is not None :
            if isinstance(json_str_or_dict, dict):
                self.__dict__ = json_str_or_dict
            else:
                self.__dict__ = json.loads(json_str_or_dict)
        else:
            self.author = ""
            self.date = ""
            self.url = ""
            self.vars_list = []#sellers and additional info
            self.rating = None
            self.text = ""
            self.essentials_list = []
            self.attached_photos_urls = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def __str__(self):
        return self.toJson()

    def fromJson(str) :
        return Comment(str)

    def is_same(self, other) :
        return self.url == other.url

class CommentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
