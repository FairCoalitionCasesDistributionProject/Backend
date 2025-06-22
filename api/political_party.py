class Political_party:
    def __init__(self, id, mandates, preferences = []):
        if mandates == 0:
            raise Exception("A party cannot have 0 mandates")
        self.id = id
        self.mandates = mandates
        self.preferences = preferences

    def getid(self):
        return self.id

    def getmandates(self):
        return self.mandates

    def getpreferences(self):
        return self.preferences

    def setpreferences(self, new_preferences):
        self.preferences = new_preferences

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        if isinstance(other, Political_party):
            return self.id == other.getid()
        return False
