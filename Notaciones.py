class Utilidades:
    """
    Clase base que contiene utilidades compartidas para el análisis
    de expresiones aritméticas y la presentación de tablas de seguimiento.
    """

    @staticmethod
    def es_operador(caracter):
        """
        Comprueba si un símbolo es un operador aritmético.
        """
        return caracter in ("+", "-", "*", "/", "^")

    @staticmethod
    def prioridad(operador):
        """
        Retorna el nivel de precedencia del operador.
        """
        prioridades = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3
        }

        return prioridades.get(operador, 0)

    @staticmethod
    def tokenizar(expresion):
        """Convierte una cadena de texto en una lista de tokens.
        Soporta:
        - Números de varios dígitos.
        - Letras.
        - Operadores.
        - Paréntesis."""
        tokens = []
        numero = ""

        for caracter in expresion:

            # Ignorar espacios
            if caracter == " ":
                continue

            # Si es un número, acumularlo
            if caracter.isdigit():

                numero += caracter

            else:

                # Si había un número acumulado,
                # agregarlo antes del nuevo símbolo
                if numero:
                    tokens.append(numero)
                    numero = ""

                tokens.append(caracter)

        # Agregar el último número
        if numero:
            tokens.append(numero)
        return tokens

    @staticmethod
    def validar_parentesis(tokens):
        """
        Valida si los paréntesis de la expresión están balanceados.
        """

        contador = 0

        for token in tokens:

            if token == "(":
                contador += 1

            elif token == ")":
                contador -= 1

                # Hay un ')' sin '(' correspondiente
                if contador < 0:
                    return False

        return contador == 0

    @staticmethod
    def mostrar_proceso(pasos, titulo="PROCESO DE CONVERSIÓN"):
        """
        Muestra la tabla de seguimiento utilizada durante
        la conversión de la expresión.
        """

        print("\n" + "-" * 110)
        print(titulo)
        print("-" * 110)

        print(
            f"{'Paso':<6}"
            f"{'Token':<10}"
            f"{'Acción':<45}"
            f"{'Pila':<18}"
            f"{'Salida'}"
        )

        print("-" * 110)

        for paso in pasos:

            pila_str = " ".join(paso["pila"])
            salida_str = " ".join(paso["salida"])

            print(
                f"{paso['paso']:<6}"
                f"{paso['token']:<10}"
                f"{paso['accion']:<45}"
                f"{pila_str:<18}"
                f"{salida_str}"
            )

    @staticmethod
    def mostrar_proceso_recorrido(
        pasos,
        titulo="PROCESO DEL RECORRIDO"
    ):
        """
        Muestra la tabla de seguimiento de un recorrido del árbol.

        La tabla contiene:
        - Paso.
        - Nodo visitado.
        - Acción realizada.
        - Recorrido acumulado.
        """

        print("\n" + "-" * 100)
        print(titulo)
        print("-" * 100)

        print(
            f"{'Paso':<8}"
            f"{'Nodo':<10}"
            f"{'Acción':<50}"
            f"{'Recorrido'}"
        )

        print("-" * 100)

        for paso in pasos:

            recorrido_str = " → ".join(
                paso["recorrido"]
            )

            print(
                f"{paso['paso']:<8}"
                f"{paso['nodo']:<10}"
                f"{paso['accion']:<50}"
                f"{recorrido_str}"
            )