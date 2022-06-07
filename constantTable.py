constantTable = {}

def getConstantByName(self, name):
        if constantTable[name]:
                return constantTable[name]
        return None

def getConstantByValue(self, value):
        for item in constantTable:
            if (item["value"] == value):
                return item
        return None

def insert(item):
        constantTable[item["name"]] = item["value"]