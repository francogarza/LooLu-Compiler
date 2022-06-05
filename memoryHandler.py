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
    localTemp = None
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

        self.localTemp = [10000, 10000]
        self.tempAddressGlobal = [12000, 12000]

        self.constAddressINT = [14000, 14000]
        self.constAddressFLOAT = [15000, 15000]
        self.constAddressCHAR = [16000, 16000]
        self.constAddressBOOL = [17000, 17000]

        self.tempPointer = [21000, 21000]
    
    def resetLocalTempMemory(self):
        self.localInt = [6000, 6000]
        self.localFloat = [7000, 7000]
        self.localChar = [8000, 8000]
        self.localBool = [9000,9000]
        self.localTemp = [10000, 10000]

    # This method is called whenever we encounter a matrix, with the base address and the dimensions we update the memory size
    def updateVariable(self, funcName, varName, varType, programName, s1, s2, dirBase):
        if funcName == programName and varType == 'int':
            newSize = dirBase + (s1 * s2)
            self.globalInt[1] = newSize
        elif funcName != programName and varType == 'int':
            newSize = dirBase + (s1 * s2)
            self.localInt[1] = newSize
        if funcName == programName and varType == 'float':
            newSize = dirBase + (s1 * s2)
            self.globalFloat[1] = newSize
        elif funcName != programName and varType == 'float':
            newSize = dirBase + (s1 * s2)
            self.localFloat[1] = newSize
        if funcName == programName and varType == 'char':
            newSize = dirBase + (s1 * s2)
            self.globalChar[1] = newSize
        elif funcName != programName and varType == 'char':
            newSize = dirBase + (s1 * s2)
            self.localChar[1] = newSize
        if funcName == programName and varType == 'bool':
            newSize = dirBase + (s1 * s2)
            self.globalBool[1] = newSize
        elif funcName != programName and varType == 'bool':
            newSize = dirBase + (s1 * s2)
            self.localBool[1] = newSize


        
    def addVariable(self, funcName, varName, varType, isParameter, programName, size):
        address = None

        if funcName == programName and varType == 'int':
            address = self.globalInt[1]
            # print('var: ', varName, 'assigned at: ', address)
            # print(size)
            if (size == None):
                self.globalInt[1] += 1
                return address
            else:
                print(self.globalInt[1], '+' , size)
                self.globalInt[1] += size
                return address
        elif funcName != programName and varType == 'int':
            address = self.localInt[1]
            if (size == None):
                self.localInt[1] += 1
                return address
            else:
                self.localInt[1] += size
                return address
        if funcName == programName and varType == 'float':
            address = self.globalFloat[1]
            # print('var: ', varName, 'assigned at: ', address)
            if (size == None):
                self.globalFloat[1] += 1
                return address
            else:
                self.globalFloat[1] += size
                return address
        elif funcName != programName and varType == 'float':
            address = self.localFloat[1]
            if (size == None):
                self.localFloat[1] += 1
                return address
            else:
                self.localFloat[1] += size
                return address
        
        if funcName == programName and varType == 'char':
            address = self.globalChar[1]
            # print('var: ', varName, 'assigned at: ', address)
            if (size == None):
                self.globalChar[1] += 1
                return address
            else:
                self.globalChar[1] += size
                return address
        elif funcName != programName and varType == 'char':
            address = self.localChar[1]
            if (size == None):
                self.localChar[1] += 1
                return address
            else:
                self.localChar[1] += size
                return address

        if funcName == programName and varType == 'bool':
            address = self.globalBool[1]
            # print('var: ', varName, 'assigned at: ', address)
            if (size == None):
                self.globalBool[1] += 1
                return address
            else:
                self.globalBool[1] += size
                return address
        elif funcName != programName and varType == 'bool':
            address = self.localBool[1]
            if (size == None):
                self.localBool[1] += 1
                return address
            else:
                self.localBool[1] += size
                return address

        if  varType == 'CTEINT':
            address = self.constAddressINT[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressINT[1] += 1
            return address

        if  varType == 'CTEFLOAT':
            address = self.constAddressFLOAT[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressFLOAT[1] += 1
            return address

        if  varType == 'CTECHAR':
            address = self.constAddressCHAR[1]
            # print('var: ', varName, 'assigned at: ', address)
            if varName in ct.constantTable:
                return ct.constantTable[varName]
            ct.constantTable[varName] = address
            self.constAddressCHAR[1] += 1
            return address

        if  varType == 'CTEBOOL':
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
            if (size == None):
                self.tempAddressGlobal[1] += 1
                return address
            else:
                self.tempAddressGlobal[1] += size
                return address
        elif funcName != programName and varType == 'TEMPORAL':
            address = self.localTemp[1]
            if (size == None):
                self.localTemp[1] += 1
                return address
            else:
                self.localTemp[1] += size
                return address
        if varType == 'POINTER':
            address = self.tempPointer[1]
            print('var: ', varName, 'assigned at: ', address)
            self.tempPointer[1] += 1
            return address