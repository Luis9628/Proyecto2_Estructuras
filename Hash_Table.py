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

    def function_hash1(self, key):
        """
        Calcula el valor hash de una clave utilizando la función SHA-256.

        Args:
            key (str): La clave a ser hasheada.

        Returns:
            int: El valor hash convertido a entero.
        """
        hash_object = hashlib.sha256(key.encode())
        hex_dig = hash_object.hexdigest()
        return int(hex_dig, 16)

    def function_hash2(self, key):
        """
        Calcula el valor hash de una clave utilizando la función MD5.

        Args:
            key (str): La clave a ser hasheada.

        Returns:
            int: El valor hash convertido a entero.
        """
        hash_object = hashlib.md5(key.encode())  # Utiliza un algoritmo de hash diferente para la segunda función hash
        hex_dig = hash_object.hexdigest()
        return int(hex_dig, 16)

    def add_symbol(self, symbol_type, name, data_type=None):
        """
        Agrega un símbolo a la tabla de símbolos.

        Args:
            symbol_type (str): El tipo de símbolo (por ejemplo, "variable" o "función").
            name (str): El nombre del símbolo.
            data_type (str, opcional): El tipo de datos asociado al símbolo.

        Returns:
            None
        """
        hash_key1 = self.function_hash1(name)
        hash_key2 = self.function_hash2(name)

        if hash_key1 not in self.symbol_table:
            self.symbol_table[hash_key1] = {"type": symbol_type, "name": name, "data_type": data_type}
        elif hash_key2 not in self.symbol_table:
            self.symbol_table[hash_key2] = {"type": symbol_type, "name": name, "data_type": data_type}
        else:
            print(f"Error semántico: '{name}' ya ha sido declarado.")

    def get_symbol_table(self):
        """
        Obtiene la tabla de símbolos actual.

        Returns:
            dict: La tabla de símbolos como un diccionario.
        """
        return self.symbol_table

    def get_symbol(self, name):
        """
        Obtén la información asociada a un símbolo por su nombre.

        Args:
            name (str): El nombre del símbolo a buscar.

        Returns:
            dict or None: La información asociada al símbolo si se encuentra, None si no se encuentra.
        """
        hash_key1 = self.function_hash1(name)
        hash_key2 = self.function_hash2(name)

        if hash_key1 in self.symbol_table:
            return self.symbol_table[hash_key1]
        elif hash_key2 in self.symbol_table:
            return self.symbol_table[hash_key2]
        else:
            return None

    def has_symbol(self, name):
        hash_key1 = self.function_hash1(name)
        hash_key2 = self.function_hash2(name)
        return hash_key1 in self.symbol_table or hash_key2 in self.symbol_table