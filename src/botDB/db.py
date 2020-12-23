import json
import os


class Database(object):
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        if os.path.exists(location):
            self.db = json.load(open(self.location, "r"))
        else:
            self.db = {}
        return True

    def set(self, key, value):
        try:
            self.db[str(key)] = [value]
            self.dumpdb()
        except Exception as e:
            print("[X] Error saving values to database : " + str(e))
            return False

    def delete(self, key):
        if key not in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True

    def append(self, key, value):
        try:
            self.db[str(key)] = self.db[str(key)] + [value]
            self.dumpdb()
        except Exception as e:
            print("[X] Error appending values to database : " + str(e))
            return False

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            print("No key can be found for " + str(key))
            return False

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, "w+"))
            return True
        except:
            return False

    def resetdb(self):
        self.db = {}
        self.dumpdb()
        return True
