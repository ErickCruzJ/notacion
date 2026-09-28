from Notaciones import Utilidades
from posfija import posfija
from prefijo import prefija
from arbol import ArbolExpresion


class Main:
    """
    Clase principal encargada de orquestar
    la ejecución del programa.
    """

    def __init__(self):

        self.conv_posfija = posfija()

        self.conv_prefija = prefija()

        self.arbol = ArbolExpresion()

    def ejecutar(self):

        # ====================================================
        # ENCABEZADO
        # ====================================================

        print("=" * 70)
        print("       CONVERSOR Y VISUALIZADOR DE ÁRBOLES")
        print("=" * 70)

        # ====================================================
        # ENTRADA
        # ====================================================

        expresion = input(
            "\nIntroduce una expresión infija "
            "(ej: (A+B)*(C-D)):\n> "
        )

        # ====================================================
        # TOKENIZACIÓN
        # ====================================================

        tokens = Utilidades.tokenizar(
            expresion
        )

        # ====================================================
        # VALIDACIÓN
        # ====================================================

        if not Utilidades.validar_parentesis(
            tokens
        ):

            print(
                "\n[ERROR] "
                "Los paréntesis no están balanceados."
            )

            return

        # ====================================================
        # EXPRESIÓN ORIGINAL
        # ====================================================

        print("\n" + "=" * 70)
        print("EXPRESIÓN INICIAL")
        print("=" * 70)

        print(
            " ".join(tokens)
        )

        # ====================================================
        #                  PREFIJA
        # ====================================================

        print("\n\n")
        print("#" * 70)
        print("                     NOTACIÓN PREFIJA")
        print("#" * 70)

        # ----------------------------------------------------
        # CONVERSIÓN A PREFIJA
        # ----------------------------------------------------

        prefijo, pasos_prefijo = (
            self.conv_prefija.convertir(
                tokens
            )
        )

        # ----------------------------------------------------
        # TABLA DE CONVERSIÓN
        # ----------------------------------------------------

        Utilidades.mostrar_proceso(
            pasos_prefijo,
            "PROCESO DE CONVERSIÓN A PREFIJO"
        )

        # ----------------------------------------------------
        # RESULTADO PREFIJO
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("RESULTADO PREFIJO")
        print("-" * 70)

        print(
            " ".join(prefijo)
        )

        # ----------------------------------------------------
        # CONSTRUIR ÁRBOL DESDE PREFIJA
        # ----------------------------------------------------

        self.arbol.construir_desde_prefija(
            prefijo
        )

        # ----------------------------------------------------
        # MOSTRAR ÁRBOL
        # ----------------------------------------------------

        print("\n")
        self.arbol.mostrar_arbol()

        # ----------------------------------------------------
        # REGLA DEL RECORRIDO
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("RECORRIDO PREFIJO")
        print("-" * 70)

        print(
            "Orden: RAÍZ → IZQUIERDA → DERECHA"
        )

        # ----------------------------------------------------
        # TABLA DEL RECORRIDO
        # ----------------------------------------------------

        pasos_recorrido_prefijo = (
            self.arbol.proceso_recorrido_prefijo()
        )

        Utilidades.mostrar_proceso_recorrido(
            pasos_recorrido_prefijo,
            "PROCESO DEL RECORRIDO PREFIJO"
        )

        # ----------------------------------------------------
        # RESULTADO DEL RECORRIDO
        # ----------------------------------------------------

        resultado_prefijo = (
            self.arbol.recorrido_prefijo()
        )

        print("\n" + "-" * 70)
        print("RESULTADO DEL RECORRIDO PREFIJO")
        print("-" * 70)

        print(
            " → ".join(
                resultado_prefijo
            )
        )

        # ====================================================
        #                  POSFIJA
        # ====================================================

        print("\n\n")
        print("#" * 70)
        print("                     NOTACIÓN POSFIJA")
        print("#" * 70)

        # ----------------------------------------------------
        # CONVERSIÓN A POSFIJA
        # ----------------------------------------------------

        posfijo, pasos_posfijo = (
            self.conv_posfija.convertir(
                tokens
            )
        )

        # ----------------------------------------------------
        # TABLA DE CONVERSIÓN
        # ----------------------------------------------------

        Utilidades.mostrar_proceso(
            pasos_posfijo,
            "PROCESO DE CONVERSIÓN A POSFIJO"
        )

        # ----------------------------------------------------
        # RESULTADO POSFIJO
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("RESULTADO POSFIJO")
        print("-" * 70)

        print(
            " ".join(posfijo)
        )

        # ----------------------------------------------------
        # CONSTRUIR ÁRBOL DESDE POSFIJA
        # ----------------------------------------------------

        self.arbol.construir_desde_posfija(
            posfijo
        )

        # ----------------------------------------------------
        # MOSTRAR ÁRBOL
        # ----------------------------------------------------

        print("\n")
        self.arbol.mostrar_arbol()

        # ----------------------------------------------------
        # REGLA DEL RECORRIDO
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("RECORRIDO POSFIJO")
        print("-" * 70)

        print(
            "Orden: IZQUIERDA → DERECHA → RAÍZ"
        )

        # ----------------------------------------------------
        # TABLA DEL RECORRIDO
        # ----------------------------------------------------

        pasos_recorrido_posfijo = (
            self.arbol.proceso_recorrido_posfijo()
        )

        Utilidades.mostrar_proceso_recorrido(
            pasos_recorrido_posfijo,
            "PROCESO DEL RECORRIDO POSFIJO"
        )

        # ----------------------------------------------------
        # RESULTADO DEL RECORRIDO
        # ----------------------------------------------------

        resultado_posfijo = (
            self.arbol.recorrido_posfijo()
        )

        print("\n" + "-" * 70)
        print("RESULTADO DEL RECORRIDO POSFIJO")
        print("-" * 70)

        print(
            " → ".join(
                resultado_posfijo
            )
        )

        # ====================================================
        #                  INFIJA
        # ====================================================

        print("\n\n")
        print("#" * 70)
        print("                     NOTACIÓN INFIJA")
        print("#" * 70)

        # ----------------------------------------------------
        # TOKENS DE LA EXPRESIÓN
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("EXPRESIÓN INFIJA")
        print("-" * 70)

        print(
            " ".join(tokens)
        )

        # ----------------------------------------------------
        # CONSTRUIR ÁRBOL DESDE INFIJA
        # ----------------------------------------------------

        self.arbol.construir_desde_infija(
            tokens
        )

        # ----------------------------------------------------
        # MOSTRAR ÁRBOL
        # ----------------------------------------------------

        print("\n")
        self.arbol.mostrar_arbol()

        # ----------------------------------------------------
        # REGLA DEL RECORRIDO
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("RECORRIDO INFIJO")
        print("-" * 70)

        print(
            "Orden: IZQUIERDA → RAÍZ → DERECHA"
        )

        # ----------------------------------------------------
        # TABLA DEL RECORRIDO
        # ----------------------------------------------------

        pasos_recorrido_infijo = (
            self.arbol.proceso_recorrido_infijo()
        )

        Utilidades.mostrar_proceso_recorrido(
            pasos_recorrido_infijo,
            "PROCESO DEL RECORRIDO INFIJO"
        )

        # ----------------------------------------------------
        # RESULTADO DEL RECORRIDO
        # ----------------------------------------------------

        resultado_infijo = (
            self.arbol.recorrido_infijo()
        )

        print("\n" + "-" * 70)
        print("RESULTADO DEL RECORRIDO INFIJO")
        print("-" * 70)

        print(
            " → ".join(
                resultado_infijo
            )
        )

        # ====================================================
        # RESUMEN
        # ====================================================

        print("\n\n")
        print("=" * 70)
        print("                         RESUMEN")
        print("=" * 70)

        print(
            "\nPrefija : "
            + " ".join(prefijo)
        )

        print(
            "Posfija : "
            + " ".join(posfijo)
        )

        print(
            "Infija  : "
            + " ".join(resultado_infijo)
        )

        print("\n" + "=" * 70)
        print("                    FIN DEL PROGRAMA")
        print("=" * 70)


# ========================================================
# EJECUCIÓN DEL PROGRAMA
# ========================================================

if __name__ == "__main__":

    app = Main()

    app.ejecutar()