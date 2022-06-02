# imports
from operator import truediv
from pickle import TRUE
from re import M
from lexer import *
from lexer import tokens
import ply.yacc as yacc
import varsTable as vt
import memoryHandler
import quadrupleGenerator
import constantTable as ct
import semanticCube as sc
import virtualMachine

# global vars
programName = None; dirFunc = vt.DirFunc(); globalVarsTable = None; currentFunc = None; currentType = None; currentParamSignature = None; currentFunctionReturnType = None; currentFunctionReturnOperand = None
currentFuncHasReturnedValue = None; currentVarTable = None; currentClass = None; currentClassVarTable = None; currentClassDirFunc = None; paramCounter = 0; currentFunctionCall = None; currentFuncDeclaration = None
qg = quadrupleGenerator.quadrupleGenerator(); mh = memoryHandler.memoryHandler()
tempCounter = 1; whileOperand = []; quadruplesOutput = []; vm = virtualMachine.virtualMachine()

# lexer
lex.lex(); print("Lexer generated")

def p_LOOLU(p):
    '''loolu : LOOLU ID np_AddGlobalFuncToDirfunc np_CreateEmptyGotomainQuadruple SEMICOLON VARS COLON np_CreateVarsTable declare_vars p_AssignGlobalVarsTable FUNCS COLON declare_funcs CLASSES COLON declare_classes LOO LEFTPAREN RIGHTPAREN np_FillGotomainQuadruple block LU SEMICOLON'''

def p_AssignGlobalVarsTable(p):
    '''p_AssignGlobalVarsTable : empty'''
    global globalVarsTable
    global dirFunc
    global programName
    row = dirFunc.getFunctionByName(programName)
    globalVarsTable = row["table"]

def p_declare_vars(p):
    '''declare_vars : vars
                    | empty'''

def p_vars(p):
    '''vars : VAR type COLON var_id SEMICOLON vars_block'''

def p_vars_block(p):
    '''vars_block : VAR type COLON var_id SEMICOLON vars_block
                  | empty'''

def p_var_id(p):
    '''var_id : ID np_AddVarToCurrentTable var_id_2
              | arr_id var_id_2'''

def p_var_id_2(p):
    '''var_id_2 : COMMA ID np_AddVarToCurrentTable var_id_2
                | COMMA arr_id var_id_2
                | empty'''

def p_arr_id(p):
    '''arr_id : ID  LEFTSQUAREBRACKET CTEINT qnp_cte_int np_addArrayToCurrentTable RIGHTSQUAREBRACKET'''

def p_np_add_array_to_current_table(p):
    '''np_addArrayToCurrentTable : empty'''
    # agrega la variable que acaba de leer a la tabla de variables actual.
    # utiliza el memory handler para asignarle una posicion en la memoria virtual.
    global currentFunc
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-4])
    if (id == None):
        address = mh.addVariable(currentFunc, p[-4], currentType, None, programName, p[-2])
        size = qg.operandStack.pop()
        qg.typeStack.pop()
        currentVarTable.insert({"name": p[-4], "type": currentType, "address": address, "size": size})
    else:
        raise Exception("ERROR: Redeclaration of variable ID = " + p[-4])

def p_declare_funcs(p):
    '''declare_funcs : funcs
                     | empty'''

def p_funcs(p):
    '''funcs : FUNC type_simple ID np_AddFunctionToDirFunc LEFTPAREN np_CreateVarsTable parameter RIGHTPAREN functionBlock np_CheckIfFuncHasReturned resetLocalMemory funcs_block'''

def p_funcs_block(p):
    '''funcs_block : FUNC type_simple ID np_AddFunctionToDirFunc LEFTPAREN np_CreateVarsTable parameter RIGHTPAREN functionBlock np_CheckIfFuncHasReturned resetLocalMemory funcs_block
                   | empty '''

def p_resetLocalMemory(p):
    '''resetLocalMemory : empty'''
    mh.resetLocalTempMemory()

def p_np_CheckIfFuncHasReturned(p):
    '''np_CheckIfFuncHasReturned : empty'''
    global currentFuncHasReturnedValue
    global currentFunc
    if currentFuncHasReturnedValue != 1:
        raise Exception('function: '+currentFunc+" is missing return value")
    else:
        if dirFunc.getFunctionByName(currentFunc)["type"] == 'void':
            # mh.resetLocalTempMemory()
            quadruplesOutput.append(('ENDFUNC','','',''))
        currentFuncHasReturnedValue = 0

# se supone que hasta aqui hacia arriba los puntos neuralgicos se documentaron y se mandaron a su segmento que esta al final del archivo
def p_parameter(p):
    '''parameter : ID COLON type_parameter np14AddParameterAsVariableToFunc parameter2
                 | empty'''

def p_typeParameter(p):
    '''type_parameter : type_simple_parameter'''

def p_typeSimpleParameter(p):
    '''type_simple_parameter : INT addToParameterSignature
                             | FLOAT addToParameterSignature
                             | CHAR addToParameterSignature
                             | BOOL addToParameterSignature
                             | VOID addToParameterSignature'''

def p_typeCompoundParameter(p):
    '''type_compound_parameter : ID'''

def p_addToParameterSignature(p):
    '''addToParameterSignature : empty'''
    global currentFunc
    global currentType
    currentType = p[-1]
    row = dirFunc.getFunctionByName(currentFunc)
    row["parameterSignature"].append(currentType)

def p_parameter2(p):
    '''parameter2 : COMMA ID COLON type_parameter np14AddParameterAsVariableToFunc parameter2
                  | empty'''

def p_function_call(p):
    '''function_call : ID np_VerifyFuncInDirFunc np_GenerateEraQuad LEFTPAREN function_call_params RIGHTPAREN np_CreateGosubQuad'''

def p_function_call2(p):
    '''function_call2 : COMMA function_call_params function_call2
                      | empty np_CheckForMissingArguments'''

def p_function_call_params(p):
    '''function_call_params : super_expression np_VerifyParamTypeWithSignature function_call2
                            | empty'''

def p_create_gosub_quad(p):
    '''np_CreateGosubQuad : empty'''
    global quadruplesOutput
    global currentFunctionCall
    jump = currentFunctionCall["functionQuadStart"]
    quadruplesOutput.append(('GOSUB','','',jump))
    # print("gosub")

def p_check_for_missing_arguments(p):
    '''np_CheckForMissingArguments : empty'''
    global paramCounter
    global currentParamSignature
    print(currentParamSignature)
    # print(currentParamSignature,paramCounter)
    if (len(currentParamSignature)-1 > paramCounter-1):
        raise Exception('Function call is missing arguments')
    else:
        pass

def p_verify_param_type_with_signature(p):
    '''np_VerifyParamTypeWithSignature : empty'''
    global currentParamSignature
    global paramCounter

    param = qg.operandStack.pop()
    paramType = qg.typeStack.pop()
    # print(param, paramType)

    if (paramType == currentParamSignature[paramCounter]):
        quadruplesOutput.append(("PARAMETER",param,paramType,("ARGUMENT#"+str(paramCounter))))
        paramCounter = paramCounter + 1
    else:
        raise Exception("Type: '" + paramType + "' does not match excepted type: '" + currentParamSignature[paramCounter] + "' for function call")

def p_np_verify_func_in_dirfunc(p):
    '''np_VerifyFuncInDirFunc : empty'''
    global dirFunc
    global currentFunctionCall
    func = dirFunc.getFunctionByName(p[-1])
    if (func == None):
        raise Exception("Could not find (",p[-1],"in the function directory")
    currentFunctionCall = func

def p_generate_era_quad(p):
    '''np_GenerateEraQuad : empty'''
    global dirFunc
    global paramCounter
    global currentParamSignature
    currentParamSignature = None
    func = dirFunc.getFunctionByName(p[-2])
    memorySize = func["memorySize"]
    funcName = func["name"]
    quadruplesOutput.append(("ERA",'empty','empty',funcName))
    paramCounter = 0
    currentParamSignature = func["parameterSignature"]
    # print(currentParamSignature)

def p_type(p):
    '''type : type_simple
            | type_compound'''

def p_type_simple(p):
    '''type_simple : INT np4SetCurrentType
                   | FLOAT np4SetCurrentType
                   | CHAR np4SetCurrentType
                   | BOOL np4SetCurrentType
                   | VOID np4SetCurrentType np_HasReturnedType'''

def p_HasReturnedType(p):
    '''np_HasReturnedType : empty'''
    global currentFuncHasReturnedValue
    currentFuncHasReturnedValue = 1

def p_type_compound(p):
    '''type_compound : ID'''

def p_function_block(p):
    '''functionBlock : LEFTBRACKET VARS COLON declare_vars np_FillMemorySizeParameterForCurrentFunc START COLON np_FillQuadStartParameterForFunc statement_block RIGHTBRACKET'''

def p_np_fill_quad_start_parameter_for_func(p):
    '''np_FillQuadStartParameterForFunc : empty'''
    global dirFunc
    global currentFunc
    row = dirFunc.getFunctionByName(currentFunc)
    row["functionQuadStart"] = len(quadruplesOutput)

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
    '''funcs_class : FUNC type_simple ID np13AddFunctionClass LEFTPAREN npCreateVarsTableForClassFunc parameter_class RIGHTPAREN block funcs_block_class'''

def p_funcs_block_class(p):
    '''funcs_block_class : FUNC type_simple ID np13AddFunctionClass LEFTPAREN npCreateVarsTableForClassFunc parameter_class RIGHTPAREN block funcs_block_class
                         | empty'''

def p_npCreateVarsTableForClassFunc(p):
    '''npCreateVarsTableForClassFunc : empty'''
    # crea y agrega la tabla de variables para la funcion actual
    # saca la fila en la que esta la funcion, busca la casilla de "table" e inicializa una tabla de variables.
    # hace la validacion de que no se hatambien se guarda la tabla de variables actual
    global currentClassDirFunc
    global currentClassFunc
    global currentClassVarTable
    row = currentClassDirFunc.getFunctionByName(currentClassFunc)
    if (row != None):
        if (row["table"] == None):
            row["table"] = vt.Vars()
            currentClassVarTable = row["table"]
            print(currentClassFunc,"row = ",row,"table",currentClassVarTable)
            # currentVarTable.printVars()
        else:
            raise Exception("ERROR: did not create vars table because vars table for funtion(", currentClassFunc, ") already exists.")
    else:
        raise Exception("ERROR: could not find function (", currentClassFunc, ") in Directory Function")

def p_parameter_class(p):
    '''parameter_class : ID COLON type_parameter_class np15AddParameterAsVariableToFuncClass parameter2_class'''

def p_typeParameterClass(p):
    '''type_parameter_class : type_simple_parameter_class'''

def p_typeSimpleParameterClass(p):
    '''type_simple_parameter_class : INT addToParameterSignatureClass
                                    | FLOAT addToParameterSignatureClass
                                    | CHAR addToParameterSignatureClass
                                    | BOOL addToParameterSignatureClass
                                    | VOID addToParameterSignatureClass'''

def p_typeCompoundParameterClass(p):
    '''type_compound_parameter_class : ID'''

def p_addToParameterSignatureClass(p):
    '''addToParameterSignatureClass : empty'''
    global currentClassFunc
    global currentType
    global currentClassDirFunc
    currentType = p[-1]
    row = currentClassDirFunc.getFunctionByName(currentClassFunc)
    row["parameterSignature"].append(currentType)
    print("asdfasd   asd s s \n\n\n",row)

def p_parameter2_class(p):
    '''parameter2_class : COMMA ID COLON type_parameter_class np15AddParameterAsVariableToFuncClass parameter2_class
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
    '''assignmentVariable : ID np16isOnCurrentVarsTable qnp1sendToQuadruples EQUAL qnp2insertOperator
                          | ID LEFTSQUAREBRACKET CTEINT RIGHTSQUAREBRACKET'''

def p_np17_test(p):
    '''np17Test : empty'''

def p_condition(p):
    '''condition : IF LEFTPAREN expression ifnp1 RIGHTPAREN block else_condition'''

def p_else_condition(p):
    '''else_condition : ELSE ifnp3else block ifnp2
                      | empty ifnp2'''

def p_ifnp3else(p):
    '''ifnp3else : empty'''
    quadruplesOutput.append(("GOTO",'empty','empty',None))
    migaja = qg.jumpStack.pop()
    siguienteQuad = len(quadruplesOutput)
    qg.jumpStack.append(siguienteQuad - 1)
    param1 = quadruplesOutput[migaja][0]
    param2 = quadruplesOutput[migaja][1]
    quadruplesOutput[migaja] = (param1,param2,'empty',siguienteQuad)

def p_ifnp1(p):
    '''ifnp1 : empty'''
    expressionType = qg.typeStack.pop()
    if (expressionType != 'bool'):
        raise Exception("Semantic Error: Type in if function is not a bool")
    else:
        expressionResult = qg.operandStack.pop()
        quadruplesOutput.append(('GOTOF', expressionResult, 'empty', None))
        currentQuadNumber = len(quadruplesOutput) - 1
        qg.jumpStack.append(currentQuadNumber)

def p_ifnp2(p):
    '''ifnp2 : empty'''
    migaja = qg.jumpStack.pop()
    siguienteQuad = len(quadruplesOutput)
    param1 = quadruplesOutput[migaja][0]
    param2 = quadruplesOutput[migaja][1]
    quadruplesOutput[migaja] = (param1,param2,'empty',siguienteQuad)

def p_writing(p):
    '''writing : PRINT LEFTPAREN print_val RIGHTPAREN SEMICOLON'''

def p_reading(p):
    '''reading : READ LEFTPAREN read_val RIGHTPAREN SEMICOLON'''

def p_while_statement(p):
    '''while_statement : WHILE LEFTPAREN np_SaveJumpForWhile expression np_CreateGotofForWhile RIGHTPAREN block np_FillGotofForWhile np_CreateGotoForWhile'''

def p_save_jump_for_while(p):
    '''np_SaveJumpForWhile : empty'''
    global quadruplesOutput
    qg.jumpStack.append(len(quadruplesOutput))

def p_create_gotof_for_while(p):
    '''np_CreateGotofForWhile : empty'''
    expressionType = qg.typeStack.pop()
    if(expressionType == 'bool'):
        expressionResult = qg.operandStack.pop()
        quadruplesOutput.append(('GOTOF',expressionResult,'',None))
        currentQuadNumber = len(quadruplesOutput) - 1
        qg.jumpStack.append(currentQuadNumber)
    else:
        raise Exception("Sematic Error: Type in while statement is not a bool")

def p_fill_gotof_for_while(p):
    '''np_FillGotofForWhile : empty'''
    migaja = qg.jumpStack.pop()
    siguienteQuad = len(quadruplesOutput) + 1
    param1 = quadruplesOutput[migaja][0]
    param2 = quadruplesOutput[migaja][1]
    quadruplesOutput[migaja] = (param1,param2,'empty',siguienteQuad)

def p_create_goto_for_while(p):
    '''np_CreateGotoForWhile : empty'''
    migaja = qg.jumpStack.pop()
    quadruplesOutput.append(('GOTO','empty','empty',migaja))


def p_return_func(p):
    '''return_func : RETURN LEFTPAREN expression np_AddReturnValueToGlobalVars RIGHTPAREN np_CreateEndFuncQuad np_ChangeHasReturnedValue
                   | empty'''

def p_np_ChangeHasReturnedValue(p):
    '''np_ChangeHasReturnedValue : empty'''
    global currentFuncHasReturnedValue
    currentFuncHasReturnedValue = 1

def p_np_add_return_to_global_vars(p):
    '''np_AddReturnValueToGlobalVars : empty'''
    global currentFunc
    global dirFunc
    global currentVarTable
    global tempCounter
    global currentFunctionReturnType
    global currentFunctionReturnOperand
    global programName
    expressionType = qg.typeStack.pop()
    address = qg.operandStack.pop()
    funcRow = dirFunc.getFunctionByName(currentFunc)
    var = globalVarsTable.getVariableByName(currentFunc)

    if (funcRow["type"] == expressionType):

        if (var == None):
            funcAddress = mh.addVariable(programName,currentFunc,funcRow['type'],None,programName,None)
            globalVarsTable.insert({"name": currentFunc, "type": expressionType, "address" : funcAddress})
        else:
            funcAddress = var["address"]
        quadruplesOutput.append(('=',address,'',funcAddress))
        currentFunctionReturnType = expressionType
        currentFunctionReturnOperand = funcAddress
    else:
        raise Exception("type: '" + expressionType + "' does not match func return type: '" + funcRow["type"] + "'")

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
               | CHARACT qnp_cte_char
               | CTECHAR qnp_cte_char
               | TRUE qnp_cte_bool
               | FALSE qnp_cte_bool
               | access_class_atribute
               | function_call np_FillStacksWithReturnValue
               | class_function_call 
               | arr_access'''
               
def p_arr_access(p):
    '''arr_access : ID LEFTSQUAREBRACKET expression np_VerifyArrAccess RIGHTSQUAREBRACKET'''

def p_np_verify_arr_access(p):
    '''np_VerifyArrAccess : empty'''
    global currentVarTable
    global globalVarsTable
    arr = currentVarTable.getVariableByName(p[-3])
    if (arr == None):
        globalVarsTable.getVariableByName(p[-3])
        if (arr == None):
            raise Exception("The array you are trying to access with name '"+p[-3]+"' has not been declared")
    type = qg.typeStack.pop()
    if(type != 'int'):
        raise Exception("An in is required to access an array. You are trying to access with '"+type+"'")
    s1 = qg.operandStack.pop()
    dirBase = arr["address"]
    quadruplesOutput.append(('VER',s1,'',arr['size']))
    pointer = mh.addVariable(None,None,'POINTER',None,None,None)
    quadruplesOutput.append(('+dirBase',dirBase,s1,pointer))
    qg.operandStack.append(pointer)
    qg.typeStack.append(type)

def p_FillStacksWithReturnValue(p):
    '''np_FillStacksWithReturnValue : empty'''
    global currentFunctionReturnType
    global currentFunctionReturnOperand
    global tempCounter
    #check if current func is not void 
    if currentFunctionCall["type"] == 'void':
        raise Exception("function: "+currentFunctionCall["name"]+" does not return a value")
    result = 'T'+str(tempCounter)
    tempCounter = tempCounter + 1
    address = mh.addVariable(currentFunc, result, 'TEMPORAL', None, programName,None)
    test = globalVarsTable.getVariableByName(currentFunctionCall['name'])
    quadruplesOutput.append(('=',test['address'],'',address))
    qg.typeStack.append(test['type'])
    qg.operandStack.append(address)
    # print(qg.operandStack)    
    # print(qg.typeStack)

def p_empty(p):
    '''empty :'''
    pass

######################
# Puntos Neuralgicos #
######################

def p_qnp_cte_int(p):
    '''qnp_cte_int : empty'''
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc, p[-1], 'CTEINT', None, programName,None)
    qg.operandStack.append(address)
    qg.typeStack.append('int')

def p_qnp_cte_float(p):
    '''qnp_cte_float : empty'''
    # print('entra FLOAT')
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc, p[-1], 'CTEFLOAT', None, programName,None)
    qg.operandStack.append(address)
    qg.typeStack.append('float')

def p_qnp_cte_char(p):
    '''qnp_cte_char : empty'''
    # print('ENTRA A CHAR',  p[-1][1])
    global currentFunc
    global programName
    address = mh.addVariable(currentFunc, p[-1][1], 'CTECHAR', None, programName,None)
    qg.operandStack.append(address)
    qg.typeStack.append('char')

def p_qnp_cte_bool(p):
    '''qnp_cte_bool : empty'''
    global currentFunc
    global programName
    # print('entra bool')
    address = mh.addVariable(currentFunc, p[-1], 'CTEBOOL', None, programName,None)
    qg.operandStack.append(address)
    qg.typeStack.append('bool')

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
        currentClassDirFunc.addVarsTable(currentClassFunc, currentClassVarTable)
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
    # print("hello",currentClassVarTable)

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
        currentClassDirFunc.insert({"name": p[-1], "type": currentType, "table": None, "parameterSignature": [], "memorySize" : 0, "functionQuadStart" : 0})
        currentClassFunc = p[-1]

def p_np14_add_parameter_as_variable_to_func(p):
    '''np14AddParameterAsVariableToFunc : empty'''
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-3])
    if (id != None):
        raise Exception("   ERROR: Redeclaration of variable ID = " + p[-3])
    else:
        address = mh.addVariable(currentFunc, p[-1], currentType, None, programName,None)
        # print(currentFunc, p[-1], currentType, None, programName,None)
        currentVarTable.insert({"name": p[-3], "type": currentType, "address" : address})

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
    print("lol",p[-3])

'''
    MAIN PROGRAM NEURALGIC POINTS
'''
def p_np16_is_on_current_vars_table(p): # Check if an ID is declared in the Global Scope
    '''np16isOnCurrentVarsTable : empty'''
    global currentVarTable
    global currentType
    global currentFunc
    global dirFunc
    global globalVarsTable

    id = currentVarTable.getVariableByName(p[-1])
    if (id == None):
        if globalVarsTable != None:
            id = globalVarsTable.getVariableByName(p[-1])
            if (id == None):
                raise Exception("   ERROR: Variable not declared on scope " + p[-1])
        else:
            raise Exception("   ERROR: Variable not declared on scope " + p[-1])
    
'''
    QUADRUPLE NEURALGIC POINTS
'''
def p_qnp1_send_to_quadruples(p):
    '''qnp1sendToQuadruples : empty'''
    # print(p[-2])
    global currentVarTable
    global globalVarsTable
    variable = currentVarTable.getVariableByName(p[-2])
    if (variable == None):
        if globalVarsTable != None:
            variable = globalVarsTable.getVariableByName(p[-2])
            if (variable == None):
                raise Exception("   ERROR: Variable not declared on scope " + p[-2])
        else:
            raise Exception("   ERROR: Variable not declared on scope " + p[-2])
    qg.operand(variable["address"], variable["type"])

def p_qnp2_insertOperator(p):
    '''qnp2insertOperator : empty'''
    qg.operator(p[-1])

def p_qnp1(p):
    '''qnp1 : empty'''
    global currentVarTable
    global globalVarsTable
    variable = currentVarTable.getVariableByName(p[-1])
    # print(variable, variable["type"])
    if(variable != None):
        qg.operandStack.append(variable["address"])
        qg.typeStack.append(variable["type"])
    else:
        variable = globalVarsTable.getVariableByName(p[-1])
        if(variable != None):
            qg.operandStack.append(variable["address"])
            qg.typeStack.append(variable["type"])
        else:
            raise Exception("could not find variable in scope nor global")

def p_qnp2(p):
    '''qnp2 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp3(p):
    '''qnp3 : empty'''
    qg.operatorStack.append(p[-1])

def p_qnp4(p):
    '''qnp4 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['+','-','*','/','%']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1
            address = mh.addVariable(currentFunc, result, 'TEMPORAL', None, programName,None)

            quadruplesOutput.append((operator, left_operand, right_operand, address))
            qg.operandStack.append(address)
            qg.typeStack.append(sc.intToType(result_type))
        else:
            raise Exception("Semantic Error -> No baila mija con el senior. " + " Mija: " + left_type + " Senior: " + right_type) 

def p_qnp5(p):
    '''qnp5 : empty'''
    global tempCounter
    if qg.operatorStack and qg.operatorStack[-1] in ['*','/','%']:
        right_operand = qg.operandStack.pop() 
        right_type = qg.typeStack.pop()
        left_operand = qg.operandStack.pop()
        left_type = qg.typeStack.pop()
        operator = qg.operatorStack.pop()
        result_type = sc.cube(left_type, right_type, operator, None, None)
        if result_type != -1:
            result = 'T'+str(tempCounter)
            tempCounter = tempCounter + 1

            address = mh.addVariable(currentFunc, result, 'TEMPORAL', None, programName,None)

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

            address = mh.addVariable(currentFunc, result, 'TEMPORAL', None, programName,None)

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

            address = mh.addVariable(currentFunc, result, 'TEMPORAL', None, programName,None)

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

    global currentVarTable

    variable = currentVarTable.getVariableByName(p[-1])
    address = variable['address']

    qg.operandStack.append(address)
    quadruplesOutput.append((qg.operatorStack[-1], '', '', qg.operandStack[-1]))

    qg.operatorStack.pop()
    qg.operandStack.pop()

def p_qnp15(p): # Insert READ to operator stack
    '''qnp15 : empty'''
    qg.operatorStack.append('READ')

def p_qnp16(p): 
    '''qnp16 : empty'''

    global currentVarTable

    variable = currentVarTable.getVariableByName(p[-1])
    address = variable['address']

    qg.operandStack.append(address)
    quadruplesOutput.append((qg.operatorStack[-1], '', '', qg.operandStack[-1]))

    qg.operatorStack.pop()
    qg.operandStack.pop()

def p_error(t):
    print("Syntax error (parser):", t.lexer.token(), t.value)
    raise Exception("Syntax error")

# puntos neuralgicos, masomenos en orden, documentados, con nombres estandarizados
def p_np_add_global_func_to_dirfunc(p):
    '''np_AddGlobalFuncToDirfunc : empty'''
    # inserta la funcion global en el directorio de funciones.
    # se guarda el nombre del programa para futura referencia
    global dirFunc
    global programName
    global currentFunc
    programName = p[-1]
    currentFunc = programName
    dirFunc.insert({"name": programName, "type": "global", "table": None})

def p_np_create_empty_gotomain_quadruple(p):
    '''np_CreateEmptyGotomainQuadruple : empty'''
    # crea el cuadruplo de GOTOMAIN vacio.
    # se llena cuando se encuentre le main. como es primer cuadruplo, no necesitamos guardar la posicion en la pila de saltos.
    global quadruplesOutput
    quadruplesOutput.append(("GOTOMAIN", 'empty', 'empty', None))

def p_np_create_vars_table(p):
    '''np_CreateVarsTable : empty'''
    # crea y agrega la tabla de variables para la funcion actual
    # saca la fila en la que esta la funcion, busca la casilla de "table" e inicializa una tabla de variables.
    # hace la validacion de que no se hatambien se guarda la tabla de variables actual
    global dirFunc
    global currentFunc
    global currentVarTable
    row = dirFunc.getFunctionByName(currentFunc)
    if (row != None):
        if (row["table"] == None):
            row["table"] = vt.Vars()
            currentVarTable = row["table"]
        else:
            raise Exception("ERROR: did not create vars table because vars table for funtion(", currentFunc, ") already exists.")
    else:
        raise Exception("ERROR: could not find function (", currentFunc, ") in Directory Function")

def p_np_add_var_to_current_table(p):
    '''np_AddVarToCurrentTable : empty'''
    # agrega la variable que acaba de leer a la tabla de variables actual.
    # utiliza el memory handler para asignarle una posicion en la memoria virtual.
    global currentFunc
    global currentVarTable
    global currentType
    id = currentVarTable.getVariableByName(p[-1])
    if (id == None):
        address = mh.addVariable(currentFunc, p[-1], currentType, None, programName,None)
        currentVarTable.insert({"name": p[-1], "type": currentType, "address": address})
        # currentVarTable.printVars()
    else:
        raise Exception("ERROR: Redeclaration of variable ID = " + p[-1])

def p_np_add_function_to_dirfunc(p):
    '''np_AddFunctionToDirFunc : empty'''
    # agrega la funcion que acaba de leer al directorio de funciones
    # valida que no se haya declarado previamente el nombre de la funcion
    # se crea con nombre y tipo y con el resto de los parametros vacios 
    # se rellenan los parametros mas adelante
    global dirFunc
    global currentFunc
    global currentType
    row = dirFunc.getFunctionByName(p[-1])
    if (row == None):
        dirFunc.insert({"name": p[-1], "type": currentType, "table": None, "parameterSignature": [], "memorySize" : 0, "functionQuadStart" : 0})
        currentFunc = p[-1]
    else:
        print("redeclaration of function " + p[-1])

def p_np_fill_memory_size_parameter_for_current_func(p):
    '''np_FillMemorySizeParameterForCurrentFunc : empty'''
    global currentFunc
    global dirFunc
    row = dirFunc.getFunctionByName(currentFunc)
    table = row["table"]
    row["memorySize"] = len(table.items)

def p_np_create_end_func_quad(p):
    '''np_CreateEndFuncQuad : empty'''
    # crea el quadruplo de endfunc por que acaba de leer el fin de la funcion
    global dirFunc
    global currentFunc
    # mh.resetLocalTempMemory()
    quadruplesOutput.append(('ENDFUNC','','',''))

def p_np_fill_gotomain_quadruple(p):
    '''np_FillGotomainQuadruple : empty'''
    # llena el cuadruplo de GOTOMAIN.
    # calculamos el cuadruplo en el que estamos que representa el primer cuadruplo del main().
    # como sabemos que es el primer cuadruplo, lo accesamos directo y meter el valor que acabamos de calcular.
    # tambien se asigna el globalVarsTable globalVarsTable
    global quadruplesOutput
    global currentVarTable
    global globalVarsTable
    global currentFunc
    firstMainFuncQuad = len(quadruplesOutput)
    quadruplesOutput[0] = (("GOTOMAIN", 'empty', 'empty', firstMainFuncQuad))
    currentVarTable = globalVarsTable
    currentFunc = programName

def p_test(p):
    '''test : empty'''
    print("testestestestest")

yacc.yacc()

parser = yacc.yacc()
print("Yacc has been generated!")

codeToCompile = open('dummyFuncs.txt','r')
data = str(codeToCompile.read())
lex.input(data)


try:
    parser.parse(data)
    print('Code passed!')
    # print(qg.operandStack  )
    # print(qg.operatorStack)
    # print(qg.typeStack)
    # print(ct.constantTable)

    file = open("objCode.txt", "w")

    temp = 0
    for quad in quadruplesOutput:
        print(temp, "-", quad)
        file.write(' '.join(str(s) for s in quad) + '\n')
        temp += 1
    
    file.write('END' + '\n')

    # for item in ct.constantTable:
    #     print(item)
    # globalVarsTable.printVars()

    file.close()
    vm.startMachine(dirFunc, mh)
    vm.runMachine(dirFunc, mh)

    # print(qg.operandStack)
    # dirFunc.printDirFunc()
    # currentVarTable.printVars()
    # globalVarsTable.printVars()
    # print(ct.constantTable)

    print('---GLOBAL DIRFUNC---') 
    dirFunc.printDirFunc()
    print('---') 
    print('---GLOBAL VARS TABLE---') 
    globalVarsTable.printVars()
    print('---') 
    tempClass = dirFunc.getFunctionByName('persona2')
    classDirFunc = tempClass['DirFunc']
    print('---CLASS DIRFUNC---') 
    classDirFunc.printDirFunc()
    classFuncInDirFunc = classDirFunc.getFunctionByName('persona2')
    classVarTable = classFuncInDirFunc['table']
    print('----')
    print('----CLASS GLOBAL VAR TABLE---') 
    classVarTable.printVars()
    print('-----')

except Exception as excep:
    print('Error in code!\n', excep)
