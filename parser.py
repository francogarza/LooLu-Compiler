# -----------------------------------------------------------------------------
# parser.py
#
# Parser para lenguaje LittleDuck2020
# -----------------------------------------------------------------------------
import sys
import ply.yacc as yacc

from lexer import tokens

# Delcaración de las reglas gramaticales

# Estructura general del programa
def p_program(p):
    '''program : PROGRAM ID SEMICOLON program_vars block'''
    p[0] = "COMPILED"

# Sección de declaración de variables
def p_program_vars(p):
    '''program_vars : vars
               | empty'''

# Definición de un bloque
def p_block(p):
    '''block : LEFTBRACKET statement_block RIGHTBRACKET'''

# Definición de un statement_block
def p_statement_block(p):
    '''statement_block : statement statement_block
                       | empty'''

# Definición de tipos de statements
def p_statement(p):
    '''statement : assignment
                 | condition
                 | writing'''

# STATEMENTS
def p_assignment(p):
    '''assignment : ID EQUALS expression SEMICOLON'''

def p_condition(p):
    '''condition : IF LEFTPAREN expression RIGHTPAREN block else_condition SEMICOLON'''

def p_writing(p):
    '''writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON'''

# Definición de la condición else
def p_else_condition(p):
    '''else_condition : ELSE block
                      | empty'''

# Definiciónes de print_val y print_exp
def p_print_val(p):
    '''print_val : expression print_exp
                 | CTESTRING print_exp'''

def p_print_exp(p):
    '''print_exp : COMMA  print_val
                 | empty'''


def p_expression(p):
    '''expression : exp comparation'''

# Definición de los operadores de comparación
def p_comparation(p):
    '''comparation : GREATER comparation_exp
                   | LESS comparation_exp
                   | NOTEQUAL comparation_exp
                   | empty'''

# Expresión de comparación
def p_comparation_exp(p):
    '''comparation_exp : exp'''

# Definición de expresión
def p_exp(p):
    '''exp : term operator'''

# Definición de los operadores de suma y resta
def p_operator(p):
    '''operator : PLUS term operator
                | MINUS term operator
                | empty'''

# Definición de un termino
def p_term(p):
    '''term : factor term_operator'''

# Definición de los operadores de multiplicación y división
def p_term_operator(p):
    '''term_operator : TIMES factor term_operator
                     | DIVIDE factor term_operator
                     | empty'''

# Definición de un factor
def p_factor(p):
    '''factor : LEFTPAREN expression RIGHTPAREN
              | sign var_cte'''

# Definición de signo de un termino
def p_sing(p):
    '''sign : PLUS
            | MINUS
            | empty'''

# Definición de la declaración de variables
def p_var_cte(p):
    '''var_cte : ID
               | CTEI
               | CTEF'''

def p_vars(p):
    '''vars : VAR var_id COLON type SEMICOLON vars_block'''

def p_var_id(p):
    '''var_id : ID var_id_2'''

def p_var_id_2(p):
    '''var_id_2 : COMMA ID var_id_2
                | empty'''

# Definición de los tipos de variables del lenguaje
def p_type(p):
    '''type : INT
            | FLOAT'''

# Definición de declaración de variables
def p_vars_block(p):
    '''vars_block : var_id COLON type SEMICOLON vars_block
                  | empty'''


# Definición del mensaje que se emitira en el error de sintaxis
def p_error(p):
    print("ERROR in iput syntax - {} ".format(p))

# Definición del epsilon/nulo/vacío
def p_empty(p):
    '''empty :'''
    pass

yacc.yacc()

# Main program del parser
if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILED":
                print("INPUT COMPILED")
        except EOFError:
            print(EOFError)
    else:
        print("File not FOUND")
