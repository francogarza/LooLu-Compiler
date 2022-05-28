import quadrupleGenerator as qg
import memoryHandler as mh
import varsTable as vt
import constantTable as ct

# Memory definition
class Memory():
    def __init__(self):
        self.data = {}
    def insert(self, address, value):
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

    # Change keys to address to get quick access
    # for key, obj in constantTable.items():
    #     constantsMemory.insert(obj['address'], obj['name'])

    def startMachine(self):
        def strToQuad(string):
            quad = list(string.split(" "))
            return quad

        def getQuads():
            quads = []
            file = open("objCode.txt", "r")
            for line in file:
                quads.append(strToQuad(line))
            return quads

        dirFunc = vt.DirFunc
        constantTable = ct.constantTable
        quadruples = getQuads()

        print(quadruples)

        

