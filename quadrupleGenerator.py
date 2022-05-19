class quadrupleGenerator:
    jumpStack = None
    migajaStack = None #Pila que almacena dirección de GOTOs pendientes
    operandStack = None
    operatorStack = None
    typeStack = None
    dimensionStack = None
    quadruplesOutput = None

    def __init__(self):
        jumpStack = []
        operandosStack = []
        operatorStack = []
        typeStack = []
        dimensionStack = []
        quadruplesOutput = []

    def operator(o):
        if o in ['*','/']:
        if o in ['+','-']:
        if o in ['&&', '||']:
        if o in ['<=','>=','<>','>','<','==']:
        if o == '=':

        #Para cada operador, implementar lógica de pops y push
    def operand(o):
        #Añadir a pila de operandos
        #Añadir a pila de tipos
        #Añadir a pila de dimensiones

    def ifStatement():
        #Haces pop a pila de operandos
        #Te aseguras que el tipo sea
        #Meter línea actual a pila de migajas
        #Generas cuadruplo GOTOF

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

    def endIfStatement():
        #Actualizas GOTOF del top de pila de migajas con línea actual

    def endElseStatement():
        #Actualizas GOTOV del top de pila de migajas con línea actual

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

    def StartWhileStatement():
        #Agregas a pila de migajas línea actual (tamaño de outputCuadruplos)
        #Generas cuadruplo GOTOF

    def EndWhileStatement():
        #Generas cuadruplo GOTO a top pila de saltos
        #Actualizas GOTOF que está en el top de las migajas con línea actual (tamaño de outputCuadruplos)

    def forStatementExpresion():
        #Guardar linea actual en pila de saltos
        #Te aseguras que el tipo de la expresion sea entero
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

    def EndForStatement():
        #Generas cuadruplo GOTO hacia top de pila de pilaSaltos
        #Actualizar top de pila de migajas con línea actual
