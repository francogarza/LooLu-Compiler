import constantTable as ct

class memoryHandler:
    functionTable = None

    # Varibles Addresses
    # Format -> [startOfSection, lastAddressAccessed]  
    # Start of section helps us to check if other section will do an overwrite and throw an error.
    globalInt = None
    globalFloat = None
    globalChar = None
    globalBool = None
    localInt = None
    localFloat = None
    localChar = None
    tempAddressGlobal = None
    constAddressINT = None
    constAddressFLOAT = None
    constAddressCHAR = None
    constAddressBOOL = None

    def __init__(self):
        self.globalInt = [2000, 2000]
        self.globalFloat = [3000, 3000]
        self.globalChar = [4000, 4000]
        self.globalBool = [5000, 5000]
        self.localInt = [6000, 6000]
        self.localFloat = [7000, 7000]
        self.localChar = [8000, 8000]
        self.localBool = [9000,9000]
        self.tempAddressGlobal = [10000, 10000]
        self.constAddressINT = [14000, 14000]
        self.constAddressFLOAT = [15000, 15000]
        self.constAddressCHAR = [16000, 16000]
        self.constAddressBOOL = [17000, 17000]
    
    def addVariable(self, funcName, varName, varType, isParameter, programName):
        address = None

        if funcName == programName and varType == 'int':
            address = self.globalInt[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.globalInt[1] += 1
            return address
        
        if funcName == programName and varType == 'float':
            address = self.globalFloat[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.globalFloat[1] += 1
            return address
        
        if funcName == programName and varType == 'char':
            address = self.globalChar[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.globalChar[1] += 1
            return address

        if funcName == programName and varType == 'bool':
            address = self.globalBool[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.globalBool[1] += 1
            return address

        if funcName == programName and varType == 'CTEINT':
            address = self.constAddressINT[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressINT[1] += 1
            return address

        if funcName == programName and varType == 'CTEFLOAT':
            address = self.constAddressFLOAT[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressFLOAT[1] += 1
            return address

        if funcName == programName and varType == 'CTECHAR':
            address = self.constAddressCHAR[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressCHAR[1] += 1
            return address

        if funcName == programName and varType == 'CTEBOOL':
            address = self.constAddressBOOL[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressBOOL[1] += 1
            return address

        if funcName == programName and varType == 'TEMPORAL':
            address = self.tempAddressGlobal[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.tempAddressGlobal[1] += 1
            return address