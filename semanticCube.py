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
               ]
             ]

cubeDimensions = [[  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '+'
                         [1,         1,      -1], #Array
                         [2,         2,       2]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '-'
                         [1,         1,      -1], #Array
                         [2,         2,       2]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '*'
                         [1,         1,       1], #Array
                         [2,         2,       2]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '*'
                         [1,         1,       1], #Array
                         [2,         2,       2]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '&&', '||'
                         [-1,       -1,      -1], #Array
                         [-1,       -1,      -1]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '<=', '>=', '<', '>'
                         [-1,       -1,      -1], #Array
                         [-1,       -1,      -1]  #Matrix
                   ],

                   [  #UniqueValue  Array  Matrix
                         [0,        -1,      -1], #UniqueValue       TYPE: '==', '<>'
                         [-1,        1,      -1], #Array
                         [-1,       -1,       2]  #Matrix
                   ]

                  ]

def typeToInt(typeInput):
    switcher = {
        'INT':   0,
        'FLOAT': 1,
        'CHAR':  2,
        'BOOL':  3,
        '+':     0,
        '-':     1,
        '*':     2,
        '/':     3,
        '&&':    4,
        '||':    4,
        '<=':    5,
        '>=':    5,
        '<>':    5,
        '<':     5,
        '>':     5,
        '==':    5,
        'UNDEF': 5,
    }
    response = switcher.get(typeInput, "Invalid Character.")
    if type(response) is int:
         return response
    else:
        print(response)
        exit(-1)

def cube(type1, type2, oper, dimension1, dimension2):
    typeResponse = cubeTypes[typeToInt(oper  )][typeToInt(type1)][typeToInt(type2)]
    dimensionResponse = cubeDimensions[typeToInt(oper) if (oper  != '<>' and oper   != '==') else 6][dimension1][dimension2]
    print("type:",typeResponse, "| dimension:", dimensionResponse)
