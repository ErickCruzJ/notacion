from Notaciones import Utilidades
from posfija import posfija
from prefijo import prefija
from arbol import ArbolExpresion

class Main:
    """Clase principal encargada de orquestar la ejecución del programa."""

    def __init__(self):
        self.conv_posfija = posfija()
        self.conv_prefija = prefija()
        self.arbol = ArbolExpresion()

    def ejecutar(self):
        print("=" * 50)
        print("       CONVERSOR Y VISUALIZADOR DE ÁRBOLES")
        print("=" * 50)

        expresion = input("\nIntroduce una expresión infija (ej: (A+B)*(C-D) ):\n> ")

        # 1. Tokenización y Validación
        tokens = Utilidades.tokenizar(expresion)
        if not Utilidades.validar_parentesis(tokens):
            print("\n[ERROR] Los paréntesis no están balanceados.")
            return
#==================================
#Prefija
#==================================
        # 1. Obtener token
        print("\n----------------------------------------")
        print("EXPRESIÓN INFIJA (TOKENS)")
        print("----------------------------------------")
        print(" ".join(tokens))

        # 2. Conversión a Prefija y Proceso
        prefijo, pasos_prefijo = self.conv_prefija.convertir(tokens)
        Utilidades.mostrar_proceso(pasos_prefijo, "PROCESO DE CONVERSIÓN A PREFIJO")

        print("\n----------------------------------------")
        print("RESULTADO PREFIJO")
        print("----------------------------------------")
        print(" ".join(prefijo))

        # 3. Construcción y Despliegue del Árbol (desde notación Prefija)
        self.arbol.construir_desde_prefija(prefijo)
        self.arbol.mostrar_arbol()
        
        # 4. Recorrido
        print("\n----------------------------------------")
        print("RECORRIDO PREFIJO DEL ÁRBOL (Preorden)")
        print("----------------------------------------")
        print(" → ".join(self.arbol.recorrido_prefijo()))

#==================================
#Posfija
#==================================
        # 1. Obtener token
        print("\n----------------------------------------")
        print("EXPRESIÓN INFIJA (TOKENS)")
        print("----------------------------------------")
        print(" ".join(tokens))

        # 2. Conversión a Posfija y Proceso
        posfija, pasos_posfija = self.conv_posfija.convertir(tokens)
        Utilidades.mostrar_proceso(pasos_posfija, "PROCESO DE CONVERSIÓN A POSFIJO")

        print("\n----------------------------------------")
        print("RESULTADO POSFIJO")
        print("----------------------------------------")
        print(" ".join(posfija))

        # 3. Construcción y Despliegue del Árbol (desde notación Posfija)
        self.arbol.construir_desde_posfija(posfija)
        self.arbol.mostrar_arbol()

        # 4. Recorrido
        print("\n----------------------------------------")
        print("RECORRIDO POSFIJO DEL ÁRBOL (Postorden)")
        print("----------------------------------------")
        print(" → ".join(self.arbol.recorrido_posfijo()))

#==================================
#Infija (recorrido)
#==================================
        # 1. Construcción y Despliegue del Árbol (desde notación Posfija)
        self.arbol.construir_desde_infija(tokens)
        self.arbol.mostrar_arbol()

        # 2. Recorrido
        print("\n----------------------------------------")
        print("RECORRIDO INFIJO DEL ÁRBOL")
        print("----------------------------------------")
        print(" → ".join(self.arbol.recorrido_infijo()))

if __name__ == "__main__":
    app = Main()
    app.ejecutar()

#Prueba