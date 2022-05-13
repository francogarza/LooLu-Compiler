from lexer import *
from parser import *

lex.lex()
print("Lexer generated")


def p_error(t):
    print("Syntax error (parser):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

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
