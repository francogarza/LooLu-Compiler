from lexer import *
from parser import *

lex.lex()
print("Lexer generated")


# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")


codeToCompile = open('dummy.txt','r')
data = str(codeToCompile.read())
lex.input(data)

try:
    parser.parse(data)
    print('Code passed!')
except:
    print('Error in code!')
