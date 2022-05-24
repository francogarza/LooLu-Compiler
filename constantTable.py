constantTable = []

def getConstantByName(self, name):
        for item in constantTable:
            if (item["name"] == name):
                return item
        return None

def insert(item):
        constantTable.append(item)