import Parser
import os

def menu():
    opcion = 0
    while True:
        print('''MENU ANALIZADOR SEMANTICO
         \t1: Línea de código
         \t2: Leer archivo de C++
         \t3: Salir''')
        try:
            opcion = int(input("Opción: ").strip())
        except ValueError:
            print("Error: Por favor, ingrese un número válido.")
            continue  # Reiniciar el bucle

        if opcion == 1:
            while True:
                linea = input("Ingrese una línea de código C++:\n")
                if linea.strip():
                    Parser.call_Parse(linea)
                    break  # Salir del bucle interno
                else:
                    print("\nIngrese código C++ válido")
            input("\nPresione enter para continuar...")
        elif opcion == 2:
            while True:
                path = input("Ingrese la dirección del archivo a analizarse:\n")
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        data = file.read()
                        Parser.call_Parse(data)
                    break  # Salir del bucle interno
                except UnicodeDecodeError:
                    print("Error: Problema con la codificación del archivo.")
            input("\nPresione enter para continuar...")
        elif opcion == 3:
            print("¡Gracias por usar este programa! ¡Viva la Liga!")
            break  # Salir del bucle principal
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == '__main__':
    menu()
