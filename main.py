from lexer import *
import ply.yacc as yacc
import varsTable as vt
from lexer import tokens

###################
### GLOBAL VARS ###
###################

dirFunc = None
currentFunc = None
currentType = None
currentVarTable = None

#############
### LEXER ###
#############

lex.lex()
print("Lexer generated")

##############
### PARSER ###
##############

def p_LOOLU(p):
    '''loolu : LOOLU ID SEMICOLON np1CreateGlobalVarsTable CLASSES COLON declare_classes VARS COLON np2CreateVarsTable declare_vars FUNCS COLON declare_funcs LOO LEFTPAREN RIGHTPAREN block LU SEMICOLON'''

def p_declare_classes(p):
    '''declare_classes : classes
               | empty'''

def p_declare_vars(p):
    '''declare_vars : vars 
               | empty'''

def p_declare_funcs(p):
    '''declare_funcs : funcs
               | empty'''

def p_classes(p):
    '''classes : CLASS ID LEFTBRACKET VARS COLON declare_vars FUNCS COLON declare_funcs RIGHTBRACKET classes_block'''

def p_vars(p):
    # '''vars : VAR type COLON var_id SEMICOLON np3AddVarToCurrentTable vars_block'''
    '''vars : VAR type COLON var_id SEMICOLON vars_block'''

def p_var_id(p):
    '''var_id : ID var_id_2'''

def p_var_id_2(p):
    '''var_id_2 : COMMA ID var_id_2
                | empty'''

def p_funcs(p):
    '''funcs : FUNC ID LEFTPAREN parameter RIGHTPAREN type_simple block funcs_block'''

def p_parameter(p):
    '''parameter : ID COLON type parameter2
                  | empty'''

def p_parameter2(p):
    '''parameter2 : COMMA parameter
                  | empty'''

def p_classes_block(p):
    '''classes_block : CLASS ID LEFTBRACKET VARS COLON declare_vars FUNCS COLON declare_funcs RIGHTBRACKET classes_block
                  | empty'''

def p_vars_block(p):
    # '''vars_block : VAR type COLON var_id SEMICOLON np3AddVarToCurrentTable vars_block
    '''vars_block : VAR type COLON var_id SEMICOLON vars_block
                  | empty'''

def p_funcs_block(p):
    '''funcs_block : FUNC ID LEFTPAREN parameter RIGHTPAREN type_simple LEFTBRACKET block RIGHTBRACKET funcs_block
                  | empty'''

def p_access_class_atribute(p):
    '''access_class_atribute : ID DOT ID '''

def p_class_function_call(p):
    '''class_function_call : ID DOT function_call'''

def p_function_call(p):
    '''function_call : ID LEFTPAREN expression function_call2 RIGHTPAREN'''

def p_function_call2(p):
    '''function_call2 : COMMA expression function_call2
                      | empty'''

def p_type(p):
    '''type : type_simple np4SetCurrentType
             | type_compound'''

def p_type_simple(p):
    '''type_simple : INT
                   | FLOAT
                   | CHAR
                   | BOOL
                   | VOID'''

def p_type_compound(p):
    '''type_compound : ID'''

def p_block(p):
    '''block : LEFTBRACKET statement_block RIGHTBRACKET'''

def p_statement_block(p):
    '''statement_block : statement statement_block
                       | empty'''

def p_statement(p):
    '''statement : assignment SEMICOLON
                 | condition
                 | while_statement
                 | writing
                 | return_func SEMICOLON
                 | function_call SEMICOLON
                 | class_function_call SEMICOLON'''

# STATEMENTS
def p_assignment(p):
    '''assignment : ID EQUAL expression
                  | ID EQUAL class_function_call
                  | access_class_atribute EQUAL expression'''

def p_condition(p):
    '''condition : IF LEFTPAREN expression RIGHTPAREN block else_condition'''

def p_writing(p):
    '''writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON'''

def p_while_statement(p):
    '''while_statement : WHILE LEFTPAREN expression RIGHTPAREN block'''

def p_return_func(p):
    '''return_func : RETURN LEFTPAREN expression RIGHTPAREN'''

def p_else_condition(p):
    '''else_condition : ELSE block
                      | empty'''

def p_print_val(p):
    '''print_val : expression print_exp'''

def p_print_exp(p):
    '''print_exp : COMMA  print_val
                 | empty'''

def p_expression(p):
    '''expression : exp comparation'''

def p_comparation(p):
    '''comparation : RELOPER comparation_exp
                   | empty'''

def p_comparation_exp(p):
    '''comparation_exp : exp'''

def p_exp(p):
    '''exp : term operator'''

# Definición de los operadores de suma y resta
def p_operator(p):
    '''operator : OPERTYPE1 term operator
                | empty'''

# Definición de un termino
def p_term(p):
    '''term : factor term_operator'''

# Definición de los operadores de multiplicación y división
def p_term_operator(p):
    '''term_operator : OPERTYPE2 factor term_operator
                     | empty'''

# Definición de un factor
def p_factor(p):
    '''factor : LEFTPAREN expression RIGHTPAREN
              | var_cte'''

# Definición de la declaración de variables
def p_var_cte(p):
    '''var_cte : ID
               | CTEINT
               | CTEFLOAT
               | access_class_atribute
               | class_function_call'''

# Definición del epsilon/nulo/vacío
def p_empty(p):
    '''empty :'''
    pass

######################
# Puntos Neuralgicos #
######################

def p_np1_create_global_vars_table(p):
    '''np1CreateGlobalVarsTable : empty'''
    global dirFunc
    global currentFunc
    dirFunc = vt.DirFunc()
    dirFunc.insert({"name": p[-1], "type": "global", "table": None})
    # dirFunc.printDirFunc()
    # print(dirFunc.dirFuncData)
    currentFunc = p[-1]

def p_np2_create_vars_table(p):
    '''np2CreateVarsTable : empty'''
    global dirFunc
    global currentVarTable
    row = dirFunc.getFunctionByName(currentFunc)
    if (row["table"] == None):
        currentVarTable = vt.Vars()
        dirFunc.addVarsTable(currentFunc, currentVarTable)

def p_np3_add_var_to_current_table(p):
    '''np3AddVarToCurrentTable : empty'''
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        print("redeclartion of variable ID " + p[-1])
    else:
        currentVarTable.insert({"name": p[-1], "type": currentType, })

def p_np4_set_current_type(p):
    '''np4SetCurrentType : empty'''
    global currenType 
    currentType = p[-1]

def p_np5_delete_dirfunc_and_current_vartable(p):
    '''np5DeleteDirfuncAndCurrentVartable : empty'''

def p_np6_set_current_type_void(p):
    '''np6SetCurrentTypeVoid : empty'''
    currentType = p[-1]

def p_np6_add_function(p):
    '''np6AddFunction : empty'''
    global currentType
    global currentFunc
    row = dirFunc.getFunctionByName(p[-1])
    if (row != None):
        print("redeclaration of function " + p[-1])
    else:
        dirFunc.insert({"name": p[-1], "type": currentType, "table": None})
        currentFunc = p[-1]

def p_np7_delete_current_vars_table(p):
    '''np6DeleteCurrentVarsTable : empty'''
    global currentVarTable
    currentVarTable = None

def p_error(t):
    print("Syntax error (parser):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

yacc.yacc()

# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")

codeToCompile = open('dummy.txt','r')
data = str(codeToCompile.read())
lex.input(data)

try:
    parser.parse(data)
    dirFunc.printDirFunc()
    print('Code passed!')
except Exception as excep: 
    print('Error in code!', excep)
