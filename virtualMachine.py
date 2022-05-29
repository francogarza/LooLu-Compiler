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
        # if address in self.data:
        #     return
        self.data[address] = value
    def get(self, address):
        if (address in self.data):
            return self.data[address]
        else:
            raise Exception('"Runtime error: Variable not found')
    def setData(self, val):
        self.data = val
    def getData(self):
        return self.data
    def printMemory(self):
        pprint.pprint(self.data)

class virtualMachine():
    dirFunc = vt.DirFunc
    constantTable = ct.constantTable
    quadruples = []

    # Memory initialization
    globalMemory = Memory()
    # localMemory = StackSegment()
    # checkpoints = qp.Stack()
    #tempLocalMemory = Memory()
    tempGlobalMemory = Memory()
    constantsMemory = Memory()

    # Variables initialization
    ip = 0
    paramsStore = []
    currentQuad = None
    currentFunc = None

    def startMachine(self):
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
        
    def runMachine(self):
        def insertInMemory(address, value):
            if (address >= 2000 and address <= 5999):
                self.globalMemory.insert(address, value)
            elif (address >= 6000 and address <= 9999):
                self.localMemory.insertTop(address, value)
            elif (address >= 10000 and address <= 13999):
                self.tempGlobalMemory.insert(address, value)
            elif (address >= 8500 and address <= 9999):
                self.localMemory.insertTopTemp(address, value)
            elif (address >= 14000 and address <= 17999):
                self.constantsMemory.insert(address, value)
        def getFromMemory(address):
            if (address >= 2000 and address <= 5999):
                return self.globalMemory.get(address)
            elif (address >= 6000 and address <= 9999):
                if self.localMemory.getTop(address) != None:
                    return self.localMemory.getTop(address)
                else:
                    return self.localMemory.getPreviousState(address)
            elif (address >= 10000 and address <= 13999):
                return self.tempGlobalMemory.get(address)
            elif (address >= 8500 and address <= 9999):
                if self.localMemory.getTopTemp(address) != None:
                    return self.localMemory.getTopTemp(address)
                else:
                    return self.localMemory.getPreviousStateTemp(address)
            elif (address >= 14000 and address <= 17999):
                return self.constantsMemory.get(address)

        currentQuad = self.quadruples[self.ip]

        while(currentQuad[0] != 'END'): # Ends program when a END is found
             # Big switch case
            if (currentQuad[0] == '='): # Assignation is found
                newVal = getFromMemory(int(currentQuad[1]))
                # resDir = getTransformmedAddress(currentQuad[3], 3)
                insertInMemory(int(currentQuad[3]), newVal)
            

            if (currentQuad[0] == '+'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
                insertInMemory(addressTemp, valLeft + valRight)

            if (currentQuad[0] == '-'): # addition is founds
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = int(currentQuad[3])
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

            if (currentQuad[0] == '<'):# Less than id found
                valLeft = getFromMemory(int(currentQuad[1]))
                valRight = getFromMemory(int(currentQuad[2]))
                addressTemp = currentQuad[3]
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
                print(val)
            
            if (currentQuad[0] == 'READ'): # Missing semantic check
                varToBeAssigned = int(currentQuad[3])
                val = input()
                # Return the type of a string that can be converted in other type 
                if val == 'true' or val == 'false':
                    print('entra')
                    insertInMemory(varToBeAssigned, val)
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            val = str(val)[0]
                            return "char"
                    insertInMemory(varToBeAssigned, val)
            
            if (currentQuad[0] == 'GOTO'): # GOTO id found
                self.ip = currentQuad[3] - 2 # -2 Because quads start at index 0 and add one more iteration
            if (currentQuad[0] == 'GOTOF'):
                val = getFromMemory(int(currentQuad[1]))
                if (val == 'false'):
                    self.ip = int(currentQuad[3]) - 1
            
            self.ip = self.ip + 1
            currentQuad = self.quadruples[self.ip]
        #     if (currentQuad[0] == '-'): # Substraction is found
        #         valLeft = getTransformmedAddress(currentQuad[1])
        #         valRight = getTransformmedAddress(currentQuad[2])
        #         addressTemp = currentQuad[3]
        #         insertInMemory(addressTemp, valLeft - valRight)
        #     if (currentQuad[0] == '*'): # Mult is found
        #         valLeft = getTransformmedAddress(currentQuad[1])
        #         valRight = getTransformmedAddress(currentQuad[2])
        #         addressTemp = currentQuad[3]
        #         insertInMemory(addressTemp, valLeft * valRight)
        #     if (currentQuad[0] == '/'): # Division is found
        #         valLeft = getTransformmedAddress(currentQuad[1])
        #         valRight = getTransformmedAddress(currentQuad[2])
        #         addressTemp = currentQuad[3]

