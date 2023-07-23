import json

class WorbotsConfig:
    data = None
    def __new__(self):
        with open("config.json", "r") as read_file:
            self.data = json.load(read_file)
        print(self.data)
    
    def getKey(self, key) -> any:
        return self.data[key]