import semanticCube as sc

class quadrupleGenerator:
    jumpStack = None
    migajaStack = None #Pila que almacena dirección de GOTOs pendientes
    operandStack = None
    operatorStack = None
    typeStack = None
    dimensionStack = None
    quadruplesOutput = None

    def __init__(self):
        self.jumpStack = []
        self.operandStack = []
        self.operatorStack = []
        self.typeStack = []
        self.dimensionStack = []
        self.quadruplesOutput = []

    def operator(o):
        if o in ['*','/']:
            pass
        if o in ['+','-']:
            pass
        if o in ['&&', '||']:
            pass
        if o in ['<=','>=','<>','>','<','==']:
            pass
        if o == '=':
            pass

    #Para cada operador, implementar lógica de pops y push
    # def operand(self, o, typ, dimensions): In next step we need the dimension for the dimension stack
    def operand(self, o, typ):
        self.operandStack.append(o) #Add to operand stack
        self.typeStack.append(typ) #Add to type stack
        # self.dimensionStack.append(dimensions) #Add to dimensions stack

    def ifStatement():
        #Haces pop a pila de operandos
        #Te aseguras que el tipo sea
        #Meter línea actual a pila de migajas
        #Generas cuadruplo GOTOF
        pass

        '''
        if(A==B+C){
        }
        else{
        }
        1. + B C T1
        2. == A T1 T2
        3. GOTOF T2  7
        4. ...
        5. ...
        6. ...
        7. GOTOV T2 9
        8. ...
        9. Termina else
        '''
    def elseStatement():
        #Meter línea actual a pila de migajas
        #Generas cuadruplo GOTOV
        pass

    def endIfStatement():
        #Actualizas GOTOF del top de pila de migajas con línea actual
        pass
    def endElseStatement():
        #Actualizas GOTOV del top de pila de migajas con línea actual
        pass
    def whileStatementExpresion():
        #Guardar linea actual en pila de saltos
        '''
        MIENTRAS(A<=B+C)HAZ{
        }
        1. + B C T1
        2. <= A T1 T2
        3. GOTOF T2  8
        4. ...
        5. ...
        6. ...
        7. GOTO 1
        8. ...
        '''
        pass

    def StartWhileStatement():
        #Agregas a pila de migajas línea actual (tamaño de outputCuadruplos)
        #Generas cuadruplo GOTOF
        pass

    def EndWhileStatement():
        #Generas cuadruplo GOTO a top pila de saltos
        #Actualizas GOTOF que está en el top de las migajas con línea actual (tamaño de outputCuadruplos)
        pass

    def forStatementExpresion():
        #Guardar linea actual en pila de saltos
        #Te aseguras que el tipo de la expresion sea entero
        pass
        '''
        DESDE X HASTA Y*5 HAZ{
        }
        1. * Y 5 T1
        2. GOTOF 6
        3. ...
        4. ...
        5. GOTO 1
        6. ...
        '''

    def StartForStatement():
        #Agregas a pila de migajas línea actual (tamaño de outputCuadruplos)
        #Generas cuadruplo GOTOF
        pass

    def EndForStatement():
        #Generas cuadruplo GOTO hacia top de pila de pilaSaltos
        #Actualizar top de pila de migajas con línea actual
        pass
