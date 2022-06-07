cubeTypes =   [[#INT  FLOAT  CHAR  BOOL
               [0,     1,    -1,   -1], #INT       TYPE: '+'
               [1,     1,    -1,   -1], #FLOAT
               [-1,   -1,     2,   -1], #CHAR
               [0,     1,    -1,    0], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [0,     1,    -1,   -1], #INT       TYPE: '-'
               [1,     1,    -1,   -1], #FLOAT
               [-1,   -1,     2,   -1], #CHAR
               [0,     1,    -1,    0], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [0,     1,    -1,    0], #INT       TYPE: '*'
               [1,     1,    -1,    0], #FLOAT
               [-1,   -1,    -1,   -1], #CHAR
               [0,     1,    -1,    0], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [0,     1,    -1,   -1], #INT       TYPE: '/'
               [1,     1,    -1,   -1], #FLOAT
               [-1,   -1,    -1,   -1], #CHAR
               [-1,    1,    -1,   -1], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [3,     3,    -1,    3], #INT       TYPE: '&&', '||'
               [3,     3,    -1,    3], #FLOAT
               [-1,   -1,    -1,   -1], #CHAR
               [3,     3,    -1,    3], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [3,     3,    -1,    3], #INT       TYPE: '<=', '>=', '<>', '<', '>', '=='
               [3,     3,    -1,    3], #FLOAT
               [-1,   -1,     3,   -1], #CHAR
               [3,     3,    -1,    3], #BOOL
               ],

               [#INT  FLOAT  CHAR  BOOL
               [0,    -1,    -1,   -1], #INT       TYPE: '='
               [1,     1,    -1,   -1], #FLOAT
               [-1,   -1,     2,   -1], #CHAR
               [-1,   -1,    -1,    3], #BOOL
               ]
             ]

def typeToInt(typeInput):
    switcher = {
        'int':   0,
        'float': 1,
        'char':  2,
        'bool':  3,
        '+':     0,
        '-':     1,
        '*':     2,
        '/':     3,
        '%':     3,
        '&&':    4,
        '||':    4,
        '<=':    5,
        '>=':    5,
        '<>':    5,
        '<':     5,
        '>':     5,
        '==':    5,
        '=':     6,
        'UNDEF': 5,
    }
    response = switcher.get(typeInput, "Invalid Character.")
    if type(response) is int:
         return response
    else:
        exit(-1)

def intToType(entero):
    switcher = {
        0:    'int',
        1:    'float',
        2:    'char',
        3:    'bool',
    }
    regresa = switcher.get(entero, "Caracter inválido.")
    return regresa

def cube(type1, type2, oper, dimension1, dimension2):
    typeResponse = cubeTypes[typeToInt(oper)][typeToInt(type1)][typeToInt(type2)]
    return typeResponse
