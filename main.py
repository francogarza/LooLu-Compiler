from lexer import *
from lexer import tokens
import ply.yacc as yacc
import varsTable as vt
import memoryHandler
import quadrupleGenerator
import constantTable as ct
import semanticCube as sc

###################
### GLOBAL VARS ###
###################

programName = None
dirFunc = None
currentFunc = None
currentType = None
currentVarTable = None
currentClass = None
currentClassVarTable = None
currentClassDirFunc = None
qg = None
mh = None
tempCounter = 1
quadruplesOutput = []
#############
### LEXER ###
#############

lex.lex()
print("Lexer generated")

qg = quadrupleGenerator.quadrupleGenerator()
mh = memoryHandler.memoryHandler()

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
                 | reading
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

def p_classes_block(p):
    '''classes_block : CLASS ID np8AddClass np9CreateGlobalVarsTableForClass LEFTBRACKET VARS COLON np10CreateVarsTableForClass declare_vars_class FUNCS COLON declare_funcs_class RIGHTBRACKET classes_block
                  | empty'''

def p_access_class_atribute(p):
    '''access_class_atribute : ID DOT ID '''

def p_class_function_call(p):
    '''class_function_call : ID DOT function_call'''

# STATEMENTS
def p_assignment(p):
    '''assignment : assignmentVariable super_expression qnp6
                  | assignmentVariable class_function_call
                  | access_class_atribute EQUAL expression'''

def p_assignment_variable(p):
    '''assignmentVariable : ID np16isOnCurrentVarsTable qnp1sendToQuadruples EQUAL qnp2insertOperator'''

def p_np17_test(p):
    '''np17Test : empty'''

def p_condition(p):
    '''condition : IF LEFTPAREN expression RIGHTPAREN block else_condition'''

def p_writing(p):
    '''writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON'''

def p_reading(p):
    '''reading : READ LEFTPAREN read_val RIGHTPAREN SEMICOLON'''

def p_while_statement(p):
    '''while_statement : WHILE LEFTPAREN expression RIGHTPAREN block'''

def p_return_func(p):
    '''return_func : RETURN LEFTPAREN expression RIGHTPAREN'''

def p_else_condition(p):
    '''else_condition : ELSE block
                      | empty'''

def p_print_val(p):
    '''print_val : qnp13 ID qnp14 print_exp'''

def p_print_exp(p):
    '''print_exp : COMMA  print_val
                 | empty'''

def p_read_val(p):
    '''read_val : qnp15 ID qnp16 read_exp'''

def p_read_exp(p):
    '''read_exp : COMMA read_val
                 | empty'''



def p_super_expression(p):
    '''super_expression : expression super_expression_helper'''

def p_super_expression_helper(p):
    '''super_expression_helper : LOGICOPERATOR qnp11 super_expression qnp12
                               | expression qnp12
                               | empty'''

def p_expression(p):
    '''expression : exp comparation qnp12'''

def p_comparation(p):
    '''comparation : RELOPER qnp9 comparation_exp 
                   | empty'''

def p_comparation_exp(p):
    '''comparation_exp : exp qnp10'''

def p_exp(p):
    '''exp : term qnp4 operator'''

def p_operator(p):
    '''operator : OPERTYPE1 qnp3 term qnp4 operator
                | empty'''

def p_term(p):
    '''term : factor qnp5 term_operator'''

def p_term_operator(p):
    '''term_operator : OPERTYPE2 qnp2 factor qnp5 term_operator
                     | empty'''

def p_factor(p):
    '''factor : LEFTPAREN qnp7 expression RIGHTPAREN qnp8
              | var_cte'''

def p_var_cte(p):
    '''var_cte : ID qnp1
               | CTEINT qnp_cte_int
               | CTEFLOAT qnp_cte_float
               | CTECHAR qnp_cte_char
               | TRUE qnp_cte_bool
               | FALSE qnp_cte_bool
               | access_class_atribute
               | class_function_call'''

def p_empty(p):
    '''empty :'''
    pass

######################
# Puntos Neuralgicos #
######################

def p_qnp_cte_int(p):
    '''qnp_cte_int : empty'''
    print('entraCTEINT')
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc["name"], p[-1], 'CTEINT', None, programName)
    qg.operandStack.append(address)
    qg.typeStack.append('int')

def p_qnp_cte_float(p):
    '''qnp_cte_float : empty'''
    print('entra FLOAT')
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc["name"], p[-1], 'CTEFLOAT', None, programName)
    qg.operandStack.append(address)
    qg.typeStack.append('float')

def p_qnp_cte_char(p):
    '''qnp_cte_char : empty'''
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc["name"], p[-1], 'CTECHAR', None, programName)
    qg.operandStack.append(address)
    qg.typeStack.append('char')

def p_qnp_cte_bool(p):
    '''qnp_cte_bool : empty'''
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc["name"], p[-1], 'CTEBOOL', None, programName)
    qg.operandStack.append(address)
    qg.typeStack.append('bool')

def p_np1_create_global_vars_table(p):
    '''np1CreateGlobalVarsTable : empty'''
    global programName
    programName = p[-1] # Save the program name on the global var
    global dirFunc
    global currentFunc
    dirFunc = vt.DirFunc()
    dirFunc.insert({"name": p[-1], "type": "global", "table": None})
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

def p_np3_add_var_to_current_table(p):
    '''np3AddVarToCurrentTable : empty'''
    global currentFunc
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-1])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-1])
    else:
        # Add to Memory
        address = mh.addVariable(currentFunc, p[-1], currentType, None, programName)
        # Add to current Var Table
        currentVarTable.insert({"name": p[-1], "type": currentType,  "address": address})
        



def p_np4_set_current_type(p):
    '''np4SetCurrentType : empty'''
    global currentType
    currentType = p[-1]

def p_np5_delete_dirfunc_and_current_vartable(p):
    '''np5DeleteDirfuncAndCurrentVartable : empty'''

def p_np6_set_current_type_void(p):
    '''np6SetCurrentTypeVoid : empty'''
    currentType = p[-1]

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
        currentClassFunc = currentClass
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

def p_np14_add_parameter_as_variable_to_func(p):
    '''np14AddParameterAsVariableToFunc : empty'''
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-3])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-3])
    else:
        currentVarTable.insert({"name": p[-3], "type": currentType})

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

'''
    MAIN PROGRAM NEURALGIC POINTS
'''
def p_np16_is_on_current_vars_table(p): # Check if an ID is declared in the Global Scope
    '''np16isOnCurrentVarsTable : empty'''
    # print("llegue")/
    global currentVarTable
    global currentType
    global currentFunc
    global dirFunc
    currentFunc = dirFunc.getFunctionByName(programName)
    currentVarTable = currentFunc["table"]

    id = currentVarTable.getVariableByName(p[-1])
    if (id == None):
        raise Exception("   ERROR: Variable not declared on scope " + p[-1])
    else:
        currentVarTable.insert({"name": p[-1], "type": currentType})
    

'''
    QUADRUPLE NEURALGIC POINTS
'''
def p_qnp1_send_to_quadruples(p):
    '''qnp1sendToQuadruples : empty'''
    # print(p[-2])
    global currentVarTable
    variable = currentVarTable.getVariableByName(p[-2])
    qg.operand(variable["address"], variable["type"])

def p_qnp2_insertOperator(p):
    '''qnp2insertOperator : empty'''
    qg.operator(p[-1])

def p_qnp1(p):
    '''qnp1 : empty'''
    global currentVarTable
    variable = currentVarTable.getVariableByName(p[-1])
    qg.operandStack.append(variable["address"])
    qg.typeStack.append(variable["type"])

def p_qnp2(p):
    '''qnp2 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp3(p):
    '''qnp3 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp4(p):
    '''qnp4 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['+','-','*','/']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1

            address = mh.addVariable(currentFunc['name'], result, 'TEMPORAL', None, programName)

            quadruplesOutput.append((operator, left_operand, right_operand, address))
            qg.operandStack.append(address)
            qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior." + "Mija: " + left_type + ".Senior: " + right_type) 

def p_qnp5(p):
    '''qnp5 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['*','/']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1

            address = mh.addVariable(currentFunc['name'], result, 'TEMPORAL', None, programName)

            quadruplesOutput.append((operator, left_operand, right_operand, address))
            qg.operandStack.append(address)
            qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior." + "Mija: " + left_type + ".Senior: " + right_type)  

def p_qnp6(p):
    '''qnp6 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['=']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            quadruplesOutput.append((operator, right_operand, '', left_operand))
            # qg.operandStack.append(result)
            # qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior." + "Mija: " + left_type + ".Senior: " + right_type) 


def p_qnp7(p):
    '''qnp7 : empty'''
    if qg.operatorStack:
        qg.operatorStack.append(p[-1])

def p_qnp8(p):
    '''qnp8 : empty'''
    if qg.operatorStack and qg.operatorStack[-1] in ['(']:
        qg.operatorStack.pop()

def p_qnp9(p):
    '''qnp9 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp10(p):
    '''qnp10 : empty'''
    global tempCounter
    global currentFunc
    if qg.operatorStack and qg.operatorStack[-1] in ['<','<=','>','>=','==']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1

            address = mh.addVariable(currentFunc['name'], result, 'TEMPORAL', None, programName)

            quadruplesOutput.append((operator, left_operand, right_operand, address))
            qg.operandStack.append(address)
            qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior." + "Mija: " + left_type + ".Senior: " + right_type) 


def p_qnp11(p):
    '''qnp11 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp12(p):
    '''qnp12 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['&&', '||']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1

            address = mh.addVariable(currentFunc['name'], result, 'TEMPORAL', None, programName)

            quadruplesOutput.append((operator, left_operand, right_operand, address))
            qg.operandStack.append(address)
            qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior." + "Mija: " + left_type + ".Senior: " + right_type) 


def p_qnp13(p): # Insert PRINT to operator stack
    '''qnp13 : empty'''
    qg.operatorStack.append('PRINT')

def p_qnp14(p): 
    '''qnp14 : empty'''

    qg.operandStack.append(p[-1])
    quadruplesOutput.append((qg.operatorStack[-1], '', '', qg.operandStack[-1]))

    qg.operatorStack.pop()
    qg.operandStack.pop()

def p_qnp15(p): # Insert READ to operator stack
    '''qnp15 : empty'''
    qg.operatorStack.append('READ')

def p_qnp16(p): 
    '''qnp16 : empty'''

    qg.operandStack.append(p[-1])
    quadruplesOutput.append((qg.operatorStack[-1], '', '', qg.operandStack[-1]))

    qg.operatorStack.pop()
    qg.operandStack.pop()

def p_error(t):
    print("Syntax error (parser):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

yacc.yacc()

# Build Yacc
parser = yacc.yacc()
print("Yacc has been generated!")


codeToCompile = open('dummy2.txt','r')
data = str(codeToCompile.read())
lex.input(data)

try:
    parser.parse(data)
    print('Code passed!')
    # print(qg.operandStack)
    # print(qg.operatorStack)
    # print(qg.typeStack)
    print(ct.constantTable)
    for quad in quadruplesOutput:
        print(quad)
    # print(quadruplesOutput)

except Exception as excep:
    print('Error in code!\n', excep)
