import ply.lex as lex
from Hash_Table import SymbolTable

# Crea una instancia de la tabla de símbolos
symbol_table = SymbolTable()

########################################################################################################################
#                                                                                                                      #
# Se crean los tokens y las palabras reservadas para tener un analizador lexico de operadores, palabras reservadas entre#
# otros                                                                                                                 #
########################################################################################################################

tokens = ["PLUS", "MINUS", "TIMES", "DIVIDE", "MODULUS", "ASSIGN", "EQUALS", "NOT", "GREATER", "LESS", "AND", "OR",
          "RPAREN", "LPAREN", "RBRACE", "LBRACE", "RBRACKET", "LBRACKET", "APOST", "QUOTE", "SEMICOLON", "COMMA",
          "DOBLEPUNTO", "COMMENT", "ID", "NUMBER", "LETTER", "POUND", "HEADER", "COMMENTBLOCK"
          ]

reserve = {
    "const": "CONST",
    "while": "WHILE",
    "for": "FOR",
    "int": "INT",
    "float": "FLOAT",
    "double": "DOUBLE",
    "string": "STRING",
    "void": "VOID",
    "if": "IF",
    "else": "ELSE",
    "endl": "ENDL",
    "do": "DO",
    "return": "RETURN",
    "define": "DEFINE",
    "include": "INCLUDE"
}

tokens = tokens + list(reserve.values())

##SE ANTEPONE \ de los tokens para el identificador, reglas de expresiones regulares y simples
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_MODULUS = r"\%"
t_ASSIGN = r"\="
t_EQUALS = r"\=\="
t_NOT = r"\!"
t_GREATER = r"\>"
t_LESS = r"\<"
t_AND = r"\&\&"
t_OR = r"\|\|"
t_RPAREN = r"\)"
t_LPAREN = r"\("
t_RBRACE = r"\}"
t_LBRACE = r"\{"
t_RBRACKET = r"\]"
t_LBRACKET = r"\["
t_APOST = r"\'"
t_QUOTE = r"\""
t_SEMICOLON = r"\;"
t_COMMA = r"\,"
t_DOBLEPUNTO = r"\:"
t_POUND = r"\#"

# Reglas par ciertas acciones
def t_COMMENT(t):
    r"\/\/.*"
    pass


def t_COMMENTBLOCK(t):
    r"\/\*(.|\n)*\*\/"
    pass


def t_HEADER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*\.h"
    return t


def get_function_body(function_name, file_path):
    """
    Esta función busca el cuerpo de una función en un archivo de código fuente.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    function_body = ""
    in_function = False

    for line in lines:
        if function_name in line:
            in_function = True
        if in_function:
            function_body += line
        if in_function and line.strip() == "":
            break

    return function_body


def analyze_function_body(function_body):
    """
    Esta función analiza el cuerpo de una función para determinar su tipo de retorno.
    En este caso, simplemente verifica si la cadena 'return 1' está en el cuerpo de la función.
    Si es así, asume que el tipo de retorno es 'int'.
    De lo contrario, devuelve 'unknown'.
    """
    if 'return 1' in function_body:
        return 'int'
    else:
        return 'unknown'


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserve.get(t.value, "ID")

    # Comprueba si el identificador ha sido declarado
    if not symbol_table.has_symbol(t.value):
        print(f"Error - Línea {t.lexer.lineno}: '{t.value}' no está declarado.")
        # Si no está declarado, puedes agregarlo a la tabla de símbolos con un tipo predeterminado (puedes ajustar según sea necesario)
        symbol_table.add_symbol("variable", t.value)
    else:
        symbol = symbol_table.get_symbol(t.value)
        if symbol['type'] == 'function':
            file_path = input("Ingrese el path del archivo para la función: ")  # Solicita al usuario el path del archivo
            function_body = get_function_body(t.value, file_path)
            return_type = analyze_function_body(function_body)
            if return_type != symbol['data_type']:
                print(
                    f"Error - Línea {t.lexer.lineno}: valor de retorno no coincide con la declaración de '{t.value}'.")

    return t

def t_NUMBER(t):
    r"\d+(\.\d+)?"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_LETTER(t):
    r"\".\""
    t.value = t.value.replace('"", ""')
    return t


# Define una regla para que podamos rastrear los números de línea
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print("Caracter incorrecto '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def tokenize(data):
    lexer.input(data)
