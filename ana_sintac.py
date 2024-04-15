import ply.yacc as yacc
from ana_lex import tokens

def p_declaraciones(p):
    '''
    declaraciones : declaracion declaraciones
                  | declaracion
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  
    else:
        p[0] = [p[1]]  

# VARIABLES
def p_declaracion(p):
    '''
    declaracion : VAR VARIABLE igual NUMERO Punto_y_coma 
                | VAR VARIABLE igual COMILLA VARIABLE COMILLA Punto_y_coma 
                | VAR VARIABLE igual TRUE Punto_y_coma 
                | VAR VARIABLE igual FALSE Punto_y_coma 
    '''
    p[0] = ('declaracion', p[1], p[2])

#CONDICIONALES IF
def p_condicional_if(p):
    '''
    declaracion : IF NUMERO Mayor_que NUMERO Dos_puntos declaraciones
                | IF NUMERO Menor_que NUMERO Dos_puntos declaraciones
                | IF NUMERO Menor_o_igual NUMERO Dos_puntos declaraciones
                | IF NUMERO Mayor_o_igual NUMERO Dos_puntos declaraciones
                | IF NUMERO igual_igual NUMERO Dos_puntos declaraciones
    '''
    p[0] = f'\nExpresion Condicional:\n {p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}'

#CICLOS FOR
def p_bucle_for(p):
    '''
    declaracion : FOR VARIABLE IN RANGE Parentesis_apertura NUMERO Parentesis_final Dos_puntos declaraciones
    '''
    p[0] = f'\nBucle For:\n {p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]} {p[7]} {p[8]} {p[9]}'

#PRINT
def p_print(p):
    '''
    declaracion : PRINT Parentesis_apertura expresion_parentesis Parentesis_final Punto_y_coma
    '''
    p[0] = f'\nPrint:\n {p[1]} {p[2]} {p[3]} {p[4]} {p[5]}'

#Contenido del print
def p_expresion_parentesis(p):
    '''
    expresion_parentesis : COMILLA variables COMILLA
                        | variables
    '''
    if len(p) == 4:
        p[0] = f'{p[1]} {p[2]} {p[3]}'
    else:
        p[0] = p[1]
        
def p_variables(p):
    '''
    variables : VARIABLE
              | NUMERO
              | variables VARIABLE
              | variables NUMERO
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]} {p[2]}'

    
#FUNCIONES

#LLAMAR A LA FUNCION
def p_function_call(p):
    '''
    declaracion : VARIABLE Parentesis_apertura Parentesis_final Punto_y_coma
                | VARIABLE Parentesis_apertura parametros Parentesis_final Punto_y_coma
    '''
    if len(p) == 6:
        p[0] = ('llamar_funcion', p[1], p[3])
    else:
        p[0] = ('llamar_funcion_sin_parametros', p[1])


def p_funcion(p):
    '''
    declaracion : DEF VARIABLE Parentesis_apertura parametros Parentesis_final Dos_puntos declaraciones
                | DEF VARIABLE Parentesis_apertura Parentesis_final Dos_puntos
    '''
    if len(p) == 8:
        p[0] = ('funcion_con_parametros', p[2], p[4], p[7])
    else:
        p[0] = ('funcion_sin_parametros', p[2])

def p_parametros(p):
    '''
    parametros : expresion
               | expresion coma parametros
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expresion(p):
    '''
    expresion : NUMERO
              | VARIABLE
    '''
    p[0] = p[1]

#MANEJO DE ERRORES
def p_error(p):
    if p:
        raise SyntaxError(f"Error. \n  Token inesperado: {p.value} en la posición {p.lexpos}")
    else:
        raise SyntaxError("Error de sintaxis. \n  Final inesperado o token faltante.")


def a_sintactico(data):
    parser = yacc.yacc(debug=True)
    try:
        result = parser.parse(data)
        if result:
            if isinstance(result, list):
                formatted_result = "\n".join(map(str, result))
                return True, formatted_result
            else:
                return False, result
        else:
            return False, "Error en el analisis."
    except SyntaxError as e:
        return False, f"{e}"
    except Exception as e:
        return False, f"Error: {str(e)}"


parser = yacc.yacc(debug=True)
