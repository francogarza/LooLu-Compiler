class Vars:
    def __init__(self):
        self.items = []
    def insert(self, item):
        self.items.append(item)
    def getVariableByName(self, name):
        for item in self.items:
            if (item["name"] == name):
                return item
        return None
    def printVars(self):
        print(self.items)
    def length(self):
        return len(self.items)
    def accessIndex(self,index):
        return self.items[index]

class DirFunc:
    def __init__(self):
        self.dirFuncData = []
    def get(self, index):
        return self.dirFuncData[index]
    def insert(self, item):
        self.dirFuncData.append(item)
    def getFunctionByName(self, name):
        for item in self.dirFuncData:
            if (item["name"] == name):
                return item
        return None
    def addVarsTable(self, name, data):
        for item in self.dirFuncData:
            if (item["name"] == name):
                item["table"] = data
                return item
        return None
    def printDirFunc(self):
        print(self.dirFuncData)
    def length(self):
        return len(self.dirFuncData)
    def accessIndex(self,index):
        return self.dirFuncData[index]
    def getGlobalVarsTable(self):
        return self.dirFuncData[0]['table']

def getFunctionByName(arr, value):
    for item in arr:
        if (item["name"] == value):
            return item
    return None