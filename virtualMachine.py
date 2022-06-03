from curses.ascii import isalpha
from cv2 import add
from pyrsistent import v
import quadrupleGenerator as qg
import memoryHandler as mh
import varsTable as vt
import constantTable as ct
import semanticCube as sc   

# Memory definition
class Memory():
    def __init__(self):
        self.data = {}
    def insert(self, address, value):
        # print('entra insert', address, value)
        # if address in self.data:
        #     return
        self.data[address] = value
    def get(self, address):
        # print("get address:",address, self.data[address])

        if (address in self.data):
            return self.data[address]
        else:
            raise Exception('"Runtime error: Variable not found')
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def printMemory(self):
        print(self.data)

class StackSegment():
    def __init__(self):
        self.data = [{}]
        self.tempLocalMemory = [{}] 
    def insertState(self):
        self.data.append({})
        self.tempLocalMemory.append({})
    def insertTop(self, address, val):
        # print('entraInsert', len(self.data)-1, address, val)
        self.data[-1][address] = val
        # print(self.data[-1])
    def insertTopTemp(self, address, val):
        self.tempLocalMemory[-1][address] = val
    def get(self, address):
        if (address in self.data):
            return self.data[address]
        else:
            Error("Runtime error: Variable not found")
    def getPreviousState(self, address):
        if (address in self.data[len(self.data)-2]):
            return self.data[-2][address]
        else:
            return None
    def getPreviousStateTemp(self, address):
        if (address in self.tempLocalMemory[-2]):
            return self.tempLocalMemory[-2][address]
        else:
            return None
    def getTop(self, address):
        if (address in self.data[-1]):
            return self.data[-1][address]
        else:
            return None
    def getTopTemp(self, address):
        if (address in self.tempLocalMemory[-1]):
            return self.tempLocalMemory[-1][address]
        else:
            return None
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def getTempLocalMem(self):
        return self.tempLocalMemory
    def getDataPrev(self):
        return self.data[-2]
    def popStack(self):
        self.data.pop()
        self.tempLocalMemory.pop()
    def printMemory(self):
        for x in self.data:
            print(x)


class virtualMachine():
    dirFunc = vt.DirFunc()
    mh = mh.memoryHandler()
    constantTable = ct.constantTable
    quadruples = []

    # Memory initialization
    globalMemory = Memory()
    localMemory = StackSegment()
    checkpoints = []
    #tempLocalMemory = Memory()
    tempGlobalMemory = Memory()
    constantsMemory = Memory()

    # Variables initialization
    ip = 0
    parameteresCheck = []
    currentQuad = None
    currentFunc = None

    def initializeArray(self, dirBase, size):
        for i in range(size):
            self.globalMemory.insert(dirBase + i, 0)

    def startMachine(self, df, mh):
        self.dirFunc = df
        self.mh = mh
        def strToQuad(string):
            quad = list(string.split(" "))
            return quad

        def readObjCode():
            file = open("objCode.txt", "r")
            for line in file:
                self.quadruples.append(strToQuad(line.strip('\n')))
        
        def loadConstantMemory():
            for key in self.constantTable:
                self.constantsMemory.insert(self.constantTable[key], key)

        readObjCode() 
        loadConstantMemory()
        
        
    def runMachine(self, dirFunc, mh):
        self.mh = mh
        print('∞Loo')
        def insertInMemory(address, value):
            if (address >= 2000 and address <= 5999):
                self.globalMemory.insert(address, value)
            elif (address >= 6000 and address <= 9999):
                self.localMemory.insertTop(address, value)
            elif (address >= 10000 and address <= 11999):
                self.localMemory.insertTopTemp(address, value)
            elif (address >= 12000 and address <= 13999):
                self.tempGlobalMemory.insert(address, value)
            elif (address >= 14000 and address <= 17999):
                self.constantsMemory.insert(address, value)
            elif (address >= 21000 and address <= 21999):
                self.globalMemory.insert(address, value)
        def getFromMemory(address):
            if (address >= 2000 and address <= 5999):
                return self.globalMemory.get(address)
            elif (address >= 6000 and address <= 9999):
                if self.localMemory.getTop(address) != None:
                    return self.localMemory.getTop(address)
                else:
                    return self.localMemory.getPreviousState(address)
            elif (address >= 10000 and address <= 11999):
                if self.localMemory.getTopTemp(address) != None:
                    return self.localMemory.getTopTemp(address)
                else:
                    return self.localMemory.getPreviousStateTemp(address)
            elif (address >= 12000 and address <= 13999):
                return self.tempGlobalMemory.get(address)
            elif (address >= 14000 and address <= 17999):
                return self.constantsMemory.get(address)
            elif (address >= 21000 and address <= 21999):
                # print(self.globalMemory.get(address), ' cague')
                self.globalMemory.get(address)
                return self.globalMemory.get(address)
        
        def getLocalAddress(type):
            if type == 'int':
                address = self.mh.localInt[1]
                self.mh.localInt[1] += 1
                return address
            if type == 'float':
                address = self.mh.localFloat[1]
                self.mh.localFloat[1] += 1
                return address
            if type == 'char':
                address = self.mh.localChar[1]
                self.mh.localChar[1] += 1
                return address
            if type == 'bool':
                address = self.mh.localBool[1]
                self.mh.localBool[1] += 1
                return address
            if type == 'temp':
                address = self.mh.localTemp[1]
                self.mh.localTemp[1] += 1
                return address


        currentQuad = self.quadruples[self.ip]

        while(currentQuad[0] != 'END'): # Ends program when a END is found
             # Big switch case
            if (currentQuad[0] == 'GOTOMAIN'):
                self.ip = int(currentQuad[3]) - 1

            if (currentQuad[0] == '='): # Assignation is found
                if (int(currentQuad[1]) >= 21000):
                    pointingAddress = getFromMemory(int(currentQuad[1]))
                    newVal = getFromMemory(pointingAddress)
                    insertInMemory(int(currentQuad[3]), newVal)
                elif (int(currentQuad[3]) >= 21000):
                    pointingAddress = getFromMemory(int(currentQuad[3]))
                    newVal = getFromMemory(int(currentQuad[1]))
                    insertInMemory(int(getFromMemory(pointerAddress)), newVal)
                else:
                    newVal = getFromMemory(int(currentQuad[1]))
                    # resDir = getTransformmedAddress(currentQuad[3], 3)
                    insertInMemory(int(currentQuad[3]), newVal)
                    # self.globalMemory.printMemory()

            

            if (currentQuad[0] == '+'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                # print(int(currentQuad[1]), int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                insertInMemory(addressTemp, valLeft + valRight)

            if (currentQuad[0] == '-'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                # print(int(currentQuad[2]), valRight)
                insertInMemory(addressTemp, valLeft - valRight)
            
            if (currentQuad[0] == '*'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                insertInMemory(addressTemp, valLeft * valRight)
            
            if (currentQuad[0] == '/'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                insertInMemory(addressTemp, valLeft / valRight)
            
            if (currentQuad[0] == '%'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                insertInMemory(addressTemp, valLeft % valRight)

            if (currentQuad[0] == '<'):# Less than id found
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                # print(valLeft, ' ', valRight)
                if (valLeft < valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '>'): # Greater than is found
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft > valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '>='):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft >= valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '<='):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft <= valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '!='):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft != valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '=='):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft == valRight):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '&&'):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft == 'true' and valRight == 'true'):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            if (currentQuad[0] == '||'):
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                if (valLeft == 'true' or valRight == 'true'):
                    insertInMemory(addressTemp, 'true')
                else:
                    insertInMemory(addressTemp, 'false')
            
            if (currentQuad[0] == 'PRINT'):
                val = getFromMemory(int(currentQuad[3]))
                if (type(val) == str):
                    pass
                print(val)
            
            if (currentQuad[0] == 'READ'): # Missing semantic check
                varToBeAssigned = int(currentQuad[3])
                val = input()
                
                # BOOL
                if val == 'true' or val == 'false':
                    # print('entra')
                    insertInMemory(varToBeAssigned, val)
                elif isalpha(val):
                    insertInMemory(varToBeAssigned, val)
                elif type(val) == int:
                    insertInMemory(varToBeAssigned, val)
                else:
                    insertInMemory(varToBeAssigned, val)
            
            if (currentQuad[0] == 'GOTO'): # GOTO id found
                self.ip = int(currentQuad[3]) - 1# -2 Because quads start at index 0 and add one more iteration
            if (currentQuad[0] == 'GOTOF'):
                val = getFromMemory(int(currentQuad[1]))
                
                if (val == 'false'):
                    self.ip = int(currentQuad[3]) - 1


            if (currentQuad[0] == 'ERA'):
                #Validate space
                func = self.dirFunc.getFunctionByName(currentQuad[3])
                parameteresCheck = func["parameterSignature"]
                self.localMemory.insertState()
                self.mh.resetLocalTempMemory()

            if (currentQuad[0] == 'PARAMETER'):
                paramType = currentQuad[2]
                address = getLocalAddress(paramType)
                # print(address)
                val = getFromMemory(int(currentQuad[1]))
                # print('entra P', val, address)
                insertInMemory(address, val)
                # self.localMemory.printMemory()

            if (currentQuad[0] == 'GOSUB'):
                saveQuad = self.ip
                self.ip = int(currentQuad[3]) - 1
                self.checkpoints.append(saveQuad)
                # print(saveQuad)

            if (currentQuad[0] == 'ENDFUNC'):
                # self.localMemory.printMemory()
                # print('ENTRA ENDFUNC')

                # if (needReturn):
                #     Error("Runtime Error: The function", currentFunc, "need to be exited by a return statement")
                if (len(self.checkpoints) > 0):
                    lastIp = self.checkpoints[-1]
                    self.checkpoints.pop()
                    self.localMemory.popStack()
                    self.ip = lastIp

            # ARRAYS #

            if (currentQuad[0] == 'VER'):
                requestedIndex = getFromMemory(int(currentQuad[1]))
                limitIndex = getFromMemory(int(currentQuad[3]))
                if (requestedIndex < 0 or requestedIndex >= limitIndex):
                    raise Exception('Out of bounds: index is not within the array limits.')


            if (currentQuad[0] == '+dirBase'):
                dirBase = int(currentQuad[1]) # 2001
                requestedIndex = getFromMemory(int(currentQuad[2])) #index
                pointerAddress = int(currentQuad[3]) #21000s
                insertInMemory(pointerAddress, dirBase + requestedIndex)
                # print(getFromMemory(pointerAddress))
        
            self.ip = self.ip + 1
            currentQuad = self.quadruples[self.ip]
        # self.localMemory.printMemory()
        print('Lu∞')

