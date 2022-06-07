import semanticCube as sc

class quadrupleGenerator:
    jumpStack = None
    migajaStack = []
    operandStack = None
    operatorStack = None
    typeStack = None
    dimensionStack = None
    quadruplesOutput = None
    tempCounter = None

    def __init__(self):
        self.jumpStack = []
        self.operandStack = []
        self.operatorStack = []
        self.typeStack = []
        self.dimensionStack = []
        self.quadruplesOutput = []
        self.tempCounter = 0
    def operand(self, o, typ):
        self.operandStack.append(o) 
        self.typeStack.append(typ)
