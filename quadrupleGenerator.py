import semanticCube as sc

class quadrupleGenerator:
    jumpStack = None
    migajaStack = None # GOTOs stack
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

    def operator(self, o):
        print(o)
        if o in ['*','/']:
            pass    
        if o in ['+','-']:
            pass
        if o in ['&&', '||']:
            pass
        if o in ['<=','>=','<>','>','<','==']:
            pass
        if o == '=':
            self.operatorStack.append(o)
            pass

    # def operand(self, o, typ, dimensions): In next step we need the dimension for the dimension stack
    def operand(self, o, typ):
        self.operandStack.append(o) #Add to operand stack
        self.typeStack.append(typ) #Add to type stack
        # self.dimensionStack.append(dimensions) #Add to dimensions stack

    def ifStatement():
        pass

    def elseStatement():
        pass

    def endIfStatement():
        pass
    def endElseStatement():
        pass
    def whileStatementExpresion():
        pass

    def StartWhileStatement():
        pass

    def EndWhileStatement():
        pass

    def forStatementExpresion():
        pass

    def StartForStatement():
        pass

    def EndForStatement():
        pass
