import json

class Comment:
    def __init__(self):
        self.author = ""
        self.date = ""
        self.link = ""
        self.vars_list = []#sellers and additional info
        self.rating = None
        self.text = ""
        self.essentials_list = []
        self.attached_photos_urls = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)

    def __str__(self):
        return self.toJson()

class CommentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Comment):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
