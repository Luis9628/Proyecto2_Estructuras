import hashlib

class SymbolTable:
    """
    Clase que representa una tabla de símbolos.

    Atributos:
        symbol_table (dict): Diccionario que almacena los símbolos y su información asociada.
    """
    def __init__(self):
        """
        Inicializa la tabla de símbolos como un diccionario vacío.
        """
        self.symbol_table = {}