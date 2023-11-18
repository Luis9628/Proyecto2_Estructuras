import ply.yacc as yacc
from Hash_Table import SymbolTable
from AnalizadorLexico import tokens, lexer
import json

success = True

# Una tabla hash simple para almacenar símbolos
symbol_table = {}

# Función para agregar un símbolo a la tabla de símbolos
def add_symbol(scope, name):
    if scope not in symbol_table:
        symbol_table[scope] = []
    symbol_table[scope].append(name)


def get_symbol_table(self):
    return self.symbol_table

# None AST
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def __str__(self) -> str:
        return (' '.join([" " + str(elem) for elem in self.children if elem is not None]) + ' ' + str(self.leaf))


# Reglas de precedencia
precedence = (
    ("right", "ASSIGN"),
    ("left", "AND", "OR"),
    ("left", "LESS", "GREATER", "EQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
)

start = "program"

def p_program(p):
    """
    program : function program
            | external-declaration program
            | empty
    """
    if (len(p) < 3):
        p[0] = ("program", '"_e_"')
    #    p[0] = Node("programa", leaf=p[1])
    else:
        p[0] = ("program", p[1], p[2])
    #    p[0] = Node("programa", [p[2]],p[1])


def p_external_declaration(p):
    """
    external-declaration : type assignment SEMICOLON
                         | array_usage SEMICOLON
                         | type array_usage SEMICOLON
                         | macro_definition
                         | file_inclusion
    """
    lengthP = len(p)
    if (lengthP == 2):
        p[0] = ("external_declaration", p[1])
    elif (lengthP == 3):
        p[0] = ("external_declaration", p[1], p[2])
    else:
        p[0] = ("external_declaration", p[1], p[2], p[3])
        if p[1] == "function":
            function_name = p[2]
            add_symbol("functions", function_name)
        else:
            variable_name = p[2]
            add_symbol("variables", variable_name)


def p_declaration(p):
    """
    declaration : type assignment SEMICOLON
                | assignment SEMICOLON
                | function_call SEMICOLON
                | array_usage SEMICOLON
                | type array_usage SEMICOLON
    """
    child = ["_e_" if item is None else item for item in p]

    p[0] = ("declaration", child)


def p_asignacion(p):
    """
    assignment : ID ASSIGN assignment
               | ID ASSIGN function_call
               | ID ASSIGN array_usage
               | array_usage ASSIGN assignment
               | ID COMMA assignment
               | NUMBER COMMA assignment
               | ID PLUS assignment
               | ID MINUS assignment
               | ID TIMES assignment
               | ID DIVIDE assignment
               | ID MODULUS assignment
               | NUMBER PLUS assignment
               | NUMBER MINUS assignment
               | NUMBER TIMES assignment
               | NUMBER DIVIDE assignment
               | NUMBER MODULUS assignment
               | APOST assignment APOST
               | LPAREN assignment RPAREN
               | MINUS assignment
               | NUMBER PLUS PLUS
               | ID PLUS PLUS
               | array_usage PLUS PLUS
               | NUMBER MINUS MINUS
               | ID MINUS MINUS
               | array_usage MINUS MINUS
               | NUMBER
               | ID
               | LETTER
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("assignment", child)


def p_function_call(p):
    """
     function_call : ID LPAREN RPAREN
                  |  ID LPAREN assignment RPAREN
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("function_call", child)


def p_array_usage(p):
    """
    array_usage : ID LBRACKET assignment RBRACKET
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("array_usage", child)


def p_function(p):
    """
    function : type ID LPAREN argument_list_option RPAREN compound_statement

    argument_list_option : argument_list
                         | empty

    argument_list : argument_list COMMA argument
                  | argument

    argument : type ID

    compound_statement : LBRACE statement_list RBRACE

    statement_list : statement_list statement
                   | empty

    statement : iteration_statement
              | declaration
              | selection_statement
              | return-statement
    """
    child = ["_e_" if item is None else item for item in p]

    p[0] = ("function", child)


def p_type(p):
    """
    type : INT
         | FLOAT
         | STRING
         | VOID
    """
    p[0] = ("type", p[1])


def p_iteration_statement(p):
    """
    iteration_statement : WHILE LPAREN expression RPAREN compound_statement
                        | WHILE LPAREN expression RPAREN statement
                        | DO compound_statement WHILE LPAREN expression RPAREN SEMICOLON
                        | DO statement WHILE LPAREN expression RPAREN SEMICOLON
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("iteration_statement", child)


def p_selection_statement(p):
    """
    selection_statement : IF LPAREN expression RPAREN compound_statement
                        | IF LPAREN expression RPAREN statement
                        | IF LPAREN expression RPAREN compound_statement ELSE compound_statement
                        | IF LPAREN expression RPAREN compound_statement ELSE statement
                        | IF LPAREN expression RPAREN statement ELSE compound_statement
                        | IF LPAREN expression RPAREN statement ELSE statement
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("selection_statement", child)


def p_return_statement(p):
    """
    return-statement : RETURN SEMICOLON
                     | RETURN expression SEMICOLON
    """

    child = ["_e_" if item is None else item for item in p]

    p[0] = ("return_statement", child)


def p_expression(p):
    """
    expression : expression EQUALS expression
               | expression LESS expression
               | expression GREATER expression
               | expression AND expression
               | expression OR expression
               | NOT expression
               | assignment
               | array_usage
    """
    child = ["_e_" if item is None else item for item in p]

    p[0] = ("expression", child)


def p_macro_definition(p):
    """
    macro_definition : POUND DEFINE ID assignment
    """
    p[0] = ("macro_definition", p[1], p[2], p[3], p[4])


def p_file_inclusion(p):
    """
    file_inclusion : POUND INCLUDE LESS HEADER GREATER
                   | POUND INCLUDE QUOTE HEADER QUOTE
    """

    p[0] = [("file_inclusion", p[1], p[2], p[3], p[4], p[5])]


# Handle empty productions
def p_empty(p):
    "empty :"
    pass


# Error rule for syntax errors
def p_error(p):
    global success
    if p:
        print("ERROR DE SINTAXIS CERCA DE: '%s', line '%s'" % (p.value, p.lineno - 1))
    success = False


# Build the parser
parser = yacc.yacc()


def call_Parse(source_code):
    # Crea una instancia de la tabla de símbolos
    symbol_table = SymbolTable()

    # Da la información al lexer
    lexer.input(source_code)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No más entradas

        # Aquí puedes agregar símbolos a la tabla de símbolos según sea necesario
        if tok.type == 'ID':
            symbol_table.add_symbol('variable', tok.value)

        print(tok)

    print("\n")
    lexer.lineno = 0

    # Parse
    ast = parser.parse(source_code)

    # Imprimir resultado
    if success:
        print("Codigo Valido")
        print(json.dumps(ast, indent=2))
        print("Tabla de Simbolos:")
        print(json.dumps(symbol_table.get_symbol_table(), indent=2))  # Imprime la tabla de símbolos
    else:
        print("Codigo Invalido")