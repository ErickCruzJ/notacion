class Utilidades:
    """
    Clase base que contiene utilidades compartidas para el análisis
    de expresiones aritméticas y la presentación de tablas de seguimiento.
    """

    @staticmethod
    def es_operador(caracter):
        """Comprueba si un símbolo es un operador aritmético."""
        return caracter in ("+", "-", "*", "/", "^")

    @staticmethod
    def prioridad(operador):
        """Retorna el nivel de precedencia del operador."""
        prioridades = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        return prioridades.get(operador, 0)

    @staticmethod
    def tokenizar(expresion):
        """
        Convierte una cadena de texto en una lista de tokens.
        Soporta números de varios dígitos, letras y operadores.
        """
        tokens = []
        numero = ""

        for caracter in expresion:
            if caracter == " ":
                continue

            if caracter.isdigit():
                numero += caracter
            else:
                if numero:
                    tokens.append(numero)
                    numero = ""
                tokens.append(caracter)

        if numero:
            tokens.append(numero)

        return tokens

    @staticmethod
    def validar_parentesis(tokens):
        """Valida si los paréntesis de la expresión están balanceados."""
        contador = 0
        for token in tokens:
            if token == "(":
                contador += 1
            elif token == ")":
                contador -= 1
                if contador < 0:
                    return False
        return contador == 0

    @staticmethod
    def mostrar_proceso(pasos, titulo="PROCESO DE CONVERSIÓN"):
        """Muestra la tabla de seguimiento del proceso de conversión."""
        print("\n----------------------------------------")
        print(titulo)
        print("----------------------------------------")
        print(
            f"{'Paso':<6}"
            f"{'Token':<8}"
            f"{'Acción':<42}"
            f"{'Pila':<15}"
            f"{'Salida'}"
        )
        print("-" * 110)

        for paso in pasos:
            pila_str = " ".join(paso["pila"])
            salida_str = " ".join(paso["salida"])
            print(
                f"{paso['paso']:<6}"
                f"{paso['token']:<8}"
                f"{paso['accion']:<42}"
                f"{pila_str:<15}"
                f"{salida_str}"
            )