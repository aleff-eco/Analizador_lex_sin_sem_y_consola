import ply.lex as lex

tokens = (
    'VAR',
    'IF',
    'FOR',
    'IN',
    'DEF',
    'PRINT',
    'TRUE',
    'FALSE',
    'VARIABLE',  
    'NUMERO',
    'COMILLA',
    'RANGE',
    'Punto_y_coma',
    'Mayor_que',
    'Menor_que',
    'Menor_o_igual',
    'Mayor_o_igual',
    'Dos_puntos',
    'igual',
    'igual_igual',
    'Parentesis_apertura',
    'Parentesis_final',
    'coma'
)

t_Punto_y_coma = r';'
t_Dos_puntos = r':'
t_igual = r'='
t_coma = r','
t_igual_igual = r'=='
t_Mayor_que = r'>'
t_Menor_que = r'<'
t_Mayor_o_igual = r'>='
t_Menor_o_igual = r'<='
t_Parentesis_apertura = r'\('
t_Parentesis_final = r'\)'
t_NUMERO = r"\d+"
t_COMILLA = r'\''


lexema = []

def t_TRUE(t):
    r'\bTrue\b'
    return t

def t_RANGE(t):
    r'\brange\b'
    return t

def t_PRINT(t):
    r'\bprint\b'
    return t

def t_FALSE(t):
    r'\bFalse\b'
    return t

def t_VAR(t):
    r'\bvar\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t

def t_DEF(t):
    r'\bdef\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t

def t_IN(t):
    r'in\b'
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  
    reserved_words = {'def', 'in', 'for', 'if', 'else', 'print', 'True', 'False', 'var', 'range'}  
    if t.value in reserved_words:
        return
    else:
        return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def a_lexico(data):
    global lexema

    analizador = lex.lex()
    analizador.input(data)

    lexema.clear()
    has_invalid_token = False

    while True:
        token = analizador.token()
        if not token:
            break
        if token.type == 'ERROR':
            has_invalid_token = True
        estado = f"{token.type} {token.value} {token.lexpos}" 
        lexema.append(estado)

    return not has_invalid_token, lexema



def t_error(t):
    global lexema
    estado = "ERROR {:16} {:4}".format(str(t.value[0]), str(t.lexpos))
    lexema.append(estado)
    t.lexer.skip(1)

analizador = lex.lex()
