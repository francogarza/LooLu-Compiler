from lexer import *
from lexer import tokens
import ply.yacc as yacc
import varsTable as vt

###################
### GLOBAL VARS ###
###################

dirFunc = None
currentFunc = None
currentType = None
currentVarTable = None
currentClass = None
currentClassVarTable = None
currentClassDirFunc = None

#############
### LEXER ###
#############

lex.lex()
print("Lexer generated")

##############
### PARSER ###
##############

def p_LOOLU(p):
    '''loolu : LOOLU ID np1CreateGlobalVarsTable SEMICOLON VARS COLON np2CreateVarsTable declare_vars FUNCS COLON declare_funcs CLASSES COLON declare_classes LOO LEFTPAREN RIGHTPAREN block LU SEMICOLON'''

def p_declare_vars(p):
    '''declare_vars : vars 
               | empty'''

def p_vars(p):
    '''vars : VAR type COLON var_id SEMICOLON vars_block'''

def p_vars_block(p):
    '''vars_block : VAR type COLON var_id SEMICOLON vars_block
                  | empty'''

def p_var_id(p):
    '''var_id : ID np3AddVarToCurrentTable var_id_2'''

def p_var_id_2(p):
    '''var_id_2 : COMMA ID np3AddVarToCurrentTable var_id_2
                | empty'''

def p_declare_funcs(p):
    '''declare_funcs : funcs
                     | empty'''

def p_funcs(p):
    '''funcs : FUNC type_simple ID np7AddFunction LEFTPAREN np2CreateVarsTable parameter RIGHTPAREN block funcs_block'''

def p_funcs_block(p):
    '''funcs_block : FUNC type_simple ID np7AddFunction LEFTPAREN np2CreateVarsTable parameter RIGHTPAREN block funcs_block
                   | empty'''

def p_parameter(p):
    '''parameter : ID COLON type np14AddParameterAsVariableToFunc parameter2'''

def p_parameter2(p):
    '''parameter2 : COMMA ID COLON type np14AddParameterAsVariableToFunc
                  | empty'''





def p_declare_funcs_class(p):
    '''declare_funcs_class : funcs_class
                           | empty'''

def p_funcs_class(p):
    '''funcs_class : FUNC type_simple ID np13AddFunctionClass LEFTPAREN np10CreateVarsTableForClass parameter_class RIGHTPAREN block funcs_block_class'''

def p_funcs_block_class(p):
    '''funcs_block_class : FUNC type_simple ID np13AddFunctionClass LEFTPAREN np10CreateVarsTableForClass parameter_class RIGHTPAREN block funcs_block_class
                         | empty'''

def p_parameter_class(p):
    '''parameter_class : ID COLON type np15AddParameterAsVariableToFuncClass parameter2_class'''

def p_parameter2_class(p):
    '''parameter2_class : COMMA ID COLON type np15AddParameterAsVariableToFuncClass
                        | empty'''







def p_np7_add_function(p):
    '''np7AddFunction : empty'''
    global currentType
    global currentFunc
    global dirFunc
    row = dirFunc.getFunctionByName(p[-1])
    if (row != None):
        print("redeclaration of function " + p[-1])
    else:
        dirFunc.insert({"name": p[-1], "type": currentType, "table": None})
        currentFunc = p[-1]


def p_np2_create_vars_table(p):
    '''np2CreateVarsTable : empty'''
    global dirFunc
    global currentVarTable
    global currentFunc
    row = dirFunc.getFunctionByName(currentFunc)
    if (row["table"] == None):
        row["table"] = vt.Vars()
        currentVarTable = row["table"]
        dirFunc.addVarsTable(currentFunc, currentVarTable)
    else: 
        raise Exception("ERROR: could not find function with that name in DirFunc")


def p_np14_add_parameter_as_variable_to_func(p):
    '''np14AddParameterAsVariableToFunc : empty'''
    global currentVarTable
    global currentType
    # currentVarTable.printVars()
    id = currentVarTable.getVariableByName(p[-3])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-3])
    else:
        currentVarTable.insert({"name": p[-3], "type": currentType})
        # print(currentFunc)
        # currentVarTable.printVars()


def p_function_call(p):
    '''function_call : ID LEFTPAREN expression function_call2 RIGHTPAREN'''

def p_function_call2(p):
    '''function_call2 : COMMA expression function_call2
                      | empty'''

def p_type(p):
    '''type : type_simple
            | type_compound'''

def p_type_simple(p):
    '''type_simple : INT np4SetCurrentType 
                   | FLOAT np4SetCurrentType
                   | CHAR np4SetCurrentType
                   | BOOL np4SetCurrentType
                   | VOID np4SetCurrentType'''

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

################
#### Clases ####
################

def p_declare_classes(p):
    '''declare_classes : classes
               | empty'''

def p_classes(p):
    '''classes : CLASS ID np8AddClass np9CreateGlobalVarsTableForClass LEFTBRACKET VARS COLON np10CreateVarsTableForClass declare_vars_class FUNCS COLON declare_funcs_class RIGHTBRACKET classes_block'''


def p_np15_add_parameter_as_variable_to_func_class(p):
    '''np15AddParameterAsVariableToFuncClass : empty'''
    global currentClassVarTable
    global currentType
    # currentVarTable.printVars()
    id = currentClassVarTable.getVariableByName(p[-3])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-3])
    else:
        currentClassVarTable.insert({"name": p[-3], "type": currentType})
        # print(currentFunc)
        # currentClassVarTable.printVars()


def p_declare_vars_class(p):
    '''declare_vars_class : vars_class 
                          | empty'''

def p_vars_class(p):
    '''vars_class : VAR type COLON var_id_class SEMICOLON vars_block_class'''
    
def p_vars_block_class(p):
    '''vars_block_class : VAR type COLON var_id_class SEMICOLON vars_block_class
                        | empty'''

def p_var_id_class(p):
    '''var_id_class : ID np12AddVarToCurrentTableClass var_id_class_2'''

def p_var_id_class_2(p):
    '''var_id_class_2 : COMMA ID np12AddVarToCurrentTableClass var_id_class_2
                      | empty'''

def p_classes_block(p):
    '''classes_block : CLASS ID np8AddClass np9CreateGlobalVarsTableForClass LEFTBRACKET VARS COLON np10CreateVarsTableForClass declare_vars_class FUNCS COLON declare_funcs_class RIGHTBRACKET classes_block
                  | empty'''

def p_access_class_atribute(p):
    '''access_class_atribute : ID DOT ID '''

def p_class_function_call(p):
    '''class_function_call : ID DOT function_call'''

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

def p_operator(p):
    '''operator : OPERTYPE1 term operator
                | empty'''

def p_term(p):
    '''term : factor term_operator'''

def p_term_operator(p):
    '''term_operator : OPERTYPE2 factor term_operator
                     | empty'''

def p_factor(p):
    '''factor : LEFTPAREN expression RIGHTPAREN
              | var_cte'''

def p_var_cte(p):
    '''var_cte : ID
               | CTEINT
               | CTEFLOAT
               | access_class_atribute
               | class_function_call'''

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
    currentFunc = p[-1]


def p_np3_add_var_to_current_table(p):
    '''np3AddVarToCurrentTable : empty'''
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-1])
    else:
        currentVarTable.insert({"name": p[-1], "type": currentType})

def p_np4_set_current_type(p):
    '''np4SetCurrentType : empty'''
    global currentType
    currentType = p[-1]

def p_np5_delete_dirfunc_and_current_vartable(p):
    '''np5DeleteDirfuncAndCurrentVartable : empty'''

def p_np6_set_current_type_void(p):
    '''np6SetCurrentTypeVoid : empty'''
    currentType = p[-1]

def p_np8_add_class(p):
    '''np8AddClass : empty'''
    global currentClass
    global dirFunc
    currentClass = p[-1]
    row = dirFunc.getFunctionByName(currentClass)
    if (row != None):
        raise Exception("redeclaration of class " + currentClass)
    else:
        dirFunc.insert({"name": currentClass, "type": "class", "DirFunc": None})

def p_np9_create_global_vars_table_for_class(p):
    '''np9CreateGlobalVarsTableForClass : empty'''
    global currentClassDirFunc
    global currentClassFunc
    global currentClass
    global dirFunc
    row = dirFunc.getFunctionByName(currentClass)
    if (row["DirFunc"] == None):
        row["DirFunc"] = vt.DirFunc()
        currentClassDirFunc = row["DirFunc"]
        currentClassDirFunc.insert({"name": currentClass, "type": "global", "table": None})
        # dirFunc.printDirFunc()
        # currentClassDirFunc.printDirFunc()
        currentClassFunc = currentClass
        # print(currentClassFunc)
    else: 
        raise Exception("ERROR: could not find function with that name in DirFunc")

def p_np10_create_vars_table_for_class(p):
    '''np10CreateVarsTableForClass : empty'''
    global currentClassDirFunc
    global currentClassVarTable
    global currentClassFunc
    row = currentClassDirFunc.getFunctionByName(currentClassFunc)
    if (row["table"] == None):
        currentClassVarTable = vt.Vars()
        currentClassDirFunc.addVarsTable(currentClassFunc, currentVarTable)
    else: 
        raise Exception("ERROR: could not find function with that name in DirFunc")

def p_np11_delete_current_vars_table(p):
    '''np11DeleteCurrentVarsTable : empty'''
    global currentVarTable
    currentVarTable = None

def p_np12_add_var_to_current_table_class(p):
    '''np12AddVarToCurrentTableClass : empty'''
    global currentClassVarTable
    global currentType
    id = currentClassVarTable.getVariableByName(p[-1])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-1])
    else:
        currentClassVarTable.insert({"name": p[-1], "type": currentType})

def p_np13_add_function_class(p):
    '''np13AddFunctionClass : empty'''
    global currentType
    global currentClassFunc
    global currentClassDirFunc
    row = currentClassDirFunc.getFunctionByName(p[-1])
    if (row != None):
        print("redeclaration of function " + p[-1])
    else:
        # print("else")
        currentClassDirFunc.insert({"name": p[-1], "type": currentType, "table": None})
        currentClassFunc = p[-1]

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
    # dirFunc.printDirFunc()
    # currentVarTable.printVars()
    # currentClassDirFunc.printDirFunc()
    # currentClassVarTable.printVars()
    print('Code passed!')
except Exception as excep: 
    print('Error in code!\n', excep)
