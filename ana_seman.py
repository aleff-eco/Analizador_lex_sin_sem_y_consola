from ana_sintac import parser
import io
import sys

class TablaDeSimbolos:
    def __init__(self):
        self.simbolos = {}
        self.funciones_con_parametros = {}
        self.funciones_sin_parametros = {}

    def agregar_variable(self, nombre, tipo):
        if nombre in self.simbolos:
            raise Exception(f"Error semántico: La variable '{nombre}' ya está declarada.")
        self.simbolos[nombre] = tipo

    def agregar_funcion_con_parametros(self, nombre, parametros):
        if nombre in self.funciones_con_parametros:
            raise Exception(f"Error semántico: La función '{nombre}' ya está declarada.")
        self.funciones_con_parametros[nombre] = parametros

    def agregar_funcion_sin_parametros(self, nombre, parametros):
        if nombre in self.funciones_sin_parametros:
            raise Exception(f"Error semántico: La función '{nombre}' ya está declarada.")
        self.funciones_sin_parametros[nombre] = None

class IfStatement:
    def __init__(self, condicion, contenido):
        self.condicion = condicion
        self.contenido = contenido

class ForLoop:
    def __init__(self, variable, rango, contenido):
        self.variable = variable
        self.rango = rango
        self.contenido = contenido


def analisis_semantico(arbol_sintactico, tabla_simbolos=None):
    if tabla_simbolos is None:
        tabla_simbolos = TablaDeSimbolos()

    if isinstance(arbol_sintactico, tuple):
        if arbol_sintactico[0] == 'declaracion':
            _, tipo, nombre = arbol_sintactico
            tabla_simbolos.agregar_variable(nombre, tipo)
        elif arbol_sintactico[0] == 'funcion_con_parametros':
            _, nombre_funcion, parametros, contenido = arbol_sintactico
            tabla_simbolos.agregar_funcion_con_parametros(nombre_funcion, parametros)
        elif arbol_sintactico[0] == 'funcion_sin_parametros':
            _, nombre_funcion = arbol_sintactico
            tabla_simbolos.agregar_funcion_sin_parametros(nombre_funcion, parametros=[])

    elif isinstance(arbol_sintactico, list):
        for nodo in arbol_sintactico:
            analisis_semantico(nodo, tabla_simbolos)

    return "Console status:"



def a_semantico(texto):
    old_stdout = sys.stdout  
    try:
        arbol_sintactico = parser.parse(texto)
        resultado = analisis_semantico(arbol_sintactico)
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        #exec
        exec(texto)

        output = new_stdout.getvalue()
        
        return resultado + '\n' + output
    except SyntaxError as e:
        return resultado
    except Exception as e:
        return f"{e}"
    finally:
        sys.stdout = old_stdout 
