
import json

class Bag :

    def __init__(self, value) :
        self.data = value

    def add_word(self, str, count = 1) :
        val = 0
        if str in self.data.keys():
            val = self.data[str]
        self.data[str] = count + val

    def add_bag(self, bag) :
        if bag is not None:
            for word, count in bag.data:
                self.add_word(word, count)

    def clone(self):
        copy = Bag({}) #WA to prevent random access to last created dict
        copy.add_bag(self)
        return copy

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False, indent = 4)

    def __str__(self):
        return self.toJson()

    def fromJson(dict):
        return Bag(dict)

    def fromJson(str) :
        b = Bag({}) #WA to prevent random access to last created dict
        b.__dict__ = json.loads(str)
        return b
