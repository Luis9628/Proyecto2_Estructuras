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