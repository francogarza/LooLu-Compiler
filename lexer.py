#!/usr/bin/python
import ply.lex as lex
import ply.yacc as yacc

# Lexer
# Palabras reservadas
reserved = {
    'LooLu': 'LOOLU', #nuestro program
    'Loo': 'LOO', #nuestro inicio de main
    'CLASSES': 'CLASSES',
    'Class': 'CLASS',
    'VARS': 'VARS',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'FUNCS': 'FUNCS',
    'func': 'FUNC',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'while': 'WHILE',
    'void': 'VOID',
    'read': 'READ',
    'print': 'PRINT',
    'read': 'READ',
    'return': 'RETURN',
    'START' : 'START',
    'Lu': "LU" #lo utilizamos para indicar que se acabo el main
}

# Tokens
tokens = [
    'LEFTPAREN', 'RIGHTPAREN',
    'LEFTBRACKET','RIGHTBRACKET',
    'LEFTSQUAREBRACKET', 'RIGHTSQUAREBRACKET',
    'OPERTYPE1', 'OPERTYPE2', 'LOGICOPERATOR',
    'ID', 'CTEINT', 'CTEFLOAT', 'CTECHAR',
    'RELOPER',
    'COLON', 'SEMICOLON', 'COMMA', 'EQUAL', 'DOT'
] + list(reserved.values())

# Definicion de las RegEx basicas que conforman el lenguaje
t_LOOLU = r'LooLu'
t_IF = r'if'
t_ELSE = r'else'
t_INT = r'int'
t_FLOAT = r'float'
t_PRINT = r'print'
t_TRUE = r'true'
t_FALSE = r'false'
t_RELOPER = r'\<\>|\<|\>|\=\='
t_LEFTBRACKET = r'\{'
t_RIGHTBRACKET = r'\}'
t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
t_LEFTSQUAREBRACKET = r'\['
t_RIGHTSQUAREBRACKET = r'\]'
t_OPERTYPE1 = r'\+|\-'
t_OPERTYPE2 = r'\*|\/|\%'
t_LOGICOPERATOR = r'(\&\&|\|\|)'
t_COLON = r':'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_EQUAL = r'\='
t_DOT = r'\.'
t_ignore = " \t"

#Definicion regex
def t_ID(t):
    r'[A-za-z]([A-za-z]|[0-9])*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CTEFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTECHAR(t):
    r'\'[a-zA-Z]\''
    t.value = t.value
    return t

def t_NEWLINE(t):
    r'\n'
    pass

def t_comment(t):
    r'\//.*'
    pass

def t_error(t):
    print("Lexical error ' {0} ' found in line ' {1} ' ".format(t.value[0], t.lineno))
    t.lexer.skip(1)
