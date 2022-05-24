class memoryHandler:
    functionTable = None

    # Varibles Addresses
    # Format -> [startOfSection, lastAddressAccessed]  
    # Start of section helps us to check if other section will do an overwrite and throw an error.
    globalInt = None
    globalFloat = None
    globalChar = None
    localInt = None
    localFloat = None
    localChar = None
    tempAddress = None
    constAddress = None

    def __init__(self):
        self.globalInt = [2000, 2000]
        self.globalFloat = [3000, 3000]
        self.globalChar = [4000, 4000]
        self.localInt = [5000, 5000]
        self.localFloat = [7000, 7000]
        self.localChar = [9000, 9000]
        self.tempAddress = [12000, 12000]
        self.constAddress = [14000, 14000]
    
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
            address = self.globalChar[1]
            # print('var: ', varName, 'assigned at: ', address)
            self.globalChar[1] += 1
            return address


        # if varName in self.tablaFunciones[funcName].tablaVariable:
        #     print("Error, variable ya fue declarada\n", varName, funcName)
        #     exit(-1)



        # if funcName == 'PROGRAMA' and varType == 'FLOAT':
        #     address = self.globalFloat[1]
        #     self.globalFloat[1] += 1

        # if funcName == 'PROGRAMA' and varType == 'CHAR':
        #     address = self.globalChar[1]
        #     self.globalChar[1] += 1

        # if funcName != 'PROGRAMA' and varType == 'INT':
        #     address = self.localInt[1]
        #     self.localInt[1] += 1

        # if funcName != 'PROGRAMA' and varType == 'FLOAT':
        #     address = self.localFloat[1]
        #     self.localFloat[1] += 1

        # if funcName != 'PROGRAMA' and varType == 'CHAR':
        #     address = self.localChar[1]
        #     self.localChar[1] += 1        

        # if funcName == 'TEMPORALES':
        #     address = self.tempAddress[1]
        #     self.tempAddress[1] += 1

        # v = Variable(varType, address)

        # if isParameter:
        #     if varType == 'INT':
        #         self.tablaFunciones[funcName].parametros += "i"
        #     if varType == 'FLOAT':
        #         self.tablaFunciones[funcName].parametros += "f"
        #     if varType == 'CHAR':
        #         self.tablaFunciones[funcName].parametros += "c"
        #     if varType == 'BOOL':
        #         self.tablaFunciones[funcName].parametros += "b"

        # self.tablaFunciones[funcName].tablaVariable[varName] = v
        # #print(self.tablaFunciones[funcName].tablaVariable)