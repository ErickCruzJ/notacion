from Notaciones import Utilidades
from posfija import posfija


class Nodo:
    """
    Representa un nodo del árbol de expresión.
    """

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolExpresion:
    """
    Gestiona la construcción, recorridos y representación
    visual del árbol sintáctico.
    """

    def __init__(self):
        self.raiz = None

    # ====================================================
    # MÉTODOS DE CONSTRUCCIÓN
    # ====================================================

    def construir_desde_prefija(self, tokens_prefijo):
        """
        Construye el árbol a partir de una expresión prefija.

        Se recorren los tokens de derecha a izquierda.

        Ejemplo:

        + A * B C

        Se procesa:

        C
        B
        *
        A
        +
        """

        pila = []

        for token in reversed(tokens_prefijo):

            # Operando
            if token.isalnum():

                nodo = Nodo(token)
                pila.append(nodo)

            # Operador
            elif Utilidades.es_operador(token):

                nodo = Nodo(token)

                # Primer elemento de la pila:
                # hijo izquierdo
                if pila:
                    nodo.izquierda = pila.pop()

                # Segundo elemento:
                # hijo derecho
                if pila:
                    nodo.derecha = pila.pop()

                pila.append(nodo)

        self.raiz = pila[0] if pila else None

        return self.raiz

    def construir_desde_posfija(self, tokens_posfijo):
        """
        Construye el árbol a partir de una expresión posfija.

        Se recorren los tokens de izquierda a derecha.

        Ejemplo:

        A B C * +

        """

        pila = []

        for token in tokens_posfijo:

            # Operando
            if token.isalnum():

                nodo = Nodo(token)
                pila.append(nodo)

            # Operador
            elif Utilidades.es_operador(token):

                nodo = Nodo(token)

                # Primer elemento que sale:
                # hijo derecho
                if pila:
                    nodo.derecha = pila.pop()

                # Segundo elemento:
                # hijo izquierdo
                if pila:
                    nodo.izquierda = pila.pop()

                pila.append(nodo)

        self.raiz = pila[0] if pila else None

        return self.raiz

    def construir_desde_infija(self, tokens_infijo):

        pila_operandos = []
        pila_operadores = []

        def procesar_operador():
            """
            Extrae un operador y sus dos operandos
            para formar un subárbol.
            """

            if (
                len(pila_operadores) > 0
                and len(pila_operandos) >= 2
            ):

                operador = pila_operadores.pop()

                nodo_operador = Nodo(operador)

                # El último operando que sale
                # es el hijo derecho
                nodo_operador.derecha = pila_operandos.pop()

                # El siguiente es el hijo izquierdo
                nodo_operador.izquierda = pila_operandos.pop()

                # Guardar el nuevo subárbol
                pila_operandos.append(nodo_operador)

        for token in tokens_infijo:

            # --------------------------------------------
            # OPERANDO
            # --------------------------------------------

            if token.isalnum():

                pila_operandos.append(
                    Nodo(token)
                )

            # --------------------------------------------
            # PARÉNTESIS IZQUIERDO
            # --------------------------------------------

            elif token == "(":

                pila_operadores.append(token)

            # --------------------------------------------
            # PARÉNTESIS DERECHO
            # --------------------------------------------

            elif token == ")":

                while (
                    pila_operadores
                    and pila_operadores[-1] != "("
                ):

                    procesar_operador()

                # Eliminar '('
                if pila_operadores:
                    pila_operadores.pop()

            # --------------------------------------------
            # OPERADOR
            # --------------------------------------------

            elif Utilidades.es_operador(token):

                while (
                    pila_operadores
                    and pila_operadores[-1] != "("
                    and
                    Utilidades.prioridad(
                        pila_operadores[-1]
                    )
                    >=
                    Utilidades.prioridad(token)
                ):

                    procesar_operador()

                pila_operadores.append(token)

        # Vaciar operadores restantes
        while pila_operadores:
            procesar_operador()

        # El árbol completo queda en la pila
        self.raiz = (
            pila_operandos[0]
            if pila_operandos
            else None
        )

        return self.raiz

    # ====================================================
    # RECORRIDO PREFIJO
    # ====================================================

    def recorrido_prefijo(self, nodo=None):
        """
        Recorrido preorden:

        RAÍZ → IZQUIERDA → DERECHA
        """

        if nodo is None and self.raiz:
            nodo = self.raiz

        recorrido = []

        def recorrer(actual):

            if actual is None:
                return

            recorrido.append(actual.valor)

            recorrer(actual.izquierda)
            recorrer(actual.derecha)

        recorrer(nodo)

        return recorrido

    def proceso_recorrido_prefijo(self):
        """
        Genera paso a paso el recorrido prefijo.

        Orden:

        RAÍZ → IZQUIERDA → DERECHA
        """

        pasos = []
        recorrido = []
        contador = 1

        def recorrer(actual):

            nonlocal contador

            if actual is None:
                return

            # Visitar nodo
            recorrido.append(
                str(actual.valor)
            )

            pasos.append({
                "paso": contador,
                "nodo": str(actual.valor),
                "accion": "Visitar raíz antes de sus hijos",
                "recorrido": recorrido.copy()
            })

            contador += 1

            # Recorrer izquierda
            recorrer(actual.izquierda)

            # Recorrer derecha
            recorrer(actual.derecha)

        recorrer(self.raiz)

        return pasos

    # ====================================================
    # RECORRIDO INFIJO
    # ====================================================

    def recorrido_infijo(self, nodo=None):
        """
        Recorrido inorden:

        IZQUIERDA → RAÍZ → DERECHA
        """

        if nodo is None and self.raiz:
            nodo = self.raiz

        recorrido = []

        def recorrer(actual):

            if actual is None:
                return

            recorrer(actual.izquierda)

            recorrido.append(actual.valor)

            recorrer(actual.derecha)

        recorrer(nodo)

        return recorrido

    def proceso_recorrido_infijo(self):
        """
        Genera paso a paso el recorrido infijo.

        Orden:

        IZQUIERDA → RAÍZ → DERECHA
        """

        pasos = []
        recorrido = []
        contador = 1

        def recorrer(actual):

            nonlocal contador

            if actual is None:
                return

            # Primero recorrer izquierda
            recorrer(actual.izquierda)

            # Después visitar el nodo
            recorrido.append(
                str(actual.valor)
            )

            pasos.append({
                "paso": contador,
                "nodo": str(actual.valor),
                "accion": "Visitar después de recorrer izquierda",
                "recorrido": recorrido.copy()
            })

            contador += 1

            # Finalmente recorrer derecha
            recorrer(actual.derecha)

        recorrer(self.raiz)

        return pasos

    # ====================================================
    # RECORRIDO POSFIJO
    # ====================================================

    def recorrido_posfijo(self, nodo=None):
        """
        Recorrido postorden:

        IZQUIERDA → DERECHA → RAÍZ
        """

        if nodo is None and self.raiz:
            nodo = self.raiz

        recorrido = []

        def recorrer(actual):

            if actual is None:
                return

            recorrer(actual.izquierda)

            recorrer(actual.derecha)

            recorrido.append(actual.valor)

        recorrer(nodo)

        return recorrido

    def proceso_recorrido_posfijo(self):
        """
        Genera paso a paso el recorrido posfijo.

        Orden:

        IZQUIERDA → DERECHA → RAÍZ
        """

        pasos = []
        recorrido = []
        contador = 1

        def recorrer(actual):

            nonlocal contador

            if actual is None:
                return

            # Recorrer izquierda
            recorrer(actual.izquierda)

            # Recorrer derecha
            recorrer(actual.derecha)

            # Finalmente visitar raíz
            recorrido.append(
                str(actual.valor)
            )

            pasos.append({
                "paso": contador,
                "nodo": str(actual.valor),
                "accion": "Visitar después de izquierda y derecha",
                "recorrido": recorrido.copy()
            })

            contador += 1

        recorrer(self.raiz)

        return pasos

    # ====================================================
    # POSICIONES DEL ÁRBOL
    # ====================================================

    def _calcular_posiciones(self, nodo):
        """
        Calcula la posición horizontal y vertical
        de cada nodo.

        Los nodos hoja reciben primero posiciones
        separadas horizontalmente.

        Después los padres se colocan en el punto medio
        de sus hijos.
        """

        posiciones = {}

        contador = [0]

        # Separación entre hojas
        ESPACIO = 10

        def recorrer(actual, nivel):

            if actual is None:
                return None

            # --------------------------------------------
            # HOJA
            # --------------------------------------------

            if (
                actual.izquierda is None
                and actual.derecha is None
            ):

                x = contador[0]

                contador[0] += ESPACIO

            else:

                # ----------------------------------------
                # CALCULAR HIJO IZQUIERDO
                # ----------------------------------------

                x_izquierda = recorrer(
                    actual.izquierda,
                    nivel + 1
                )

                # ----------------------------------------
                # CALCULAR HIJO DERECHO
                # ----------------------------------------

                x_derecha = recorrer(
                    actual.derecha,
                    nivel + 1
                )

                # ----------------------------------------
                # AMBOS HIJOS
                # ----------------------------------------

                if (
                    x_izquierda is not None
                    and x_derecha is not None
                ):

                    x = (
                        x_izquierda
                        + x_derecha
                    ) // 2

                # ----------------------------------------
                # SOLO HIJO IZQUIERDO
                # ----------------------------------------

                elif x_izquierda is not None:

                    x = x_izquierda

                # ----------------------------------------
                # SOLO HIJO DERECHO
                # ----------------------------------------

                else:

                    x = x_derecha

            posiciones[id(actual)] = (
                x,
                nivel
            )

            return x

        recorrer(nodo, 0)

        return posiciones

    # ====================================================
    # OBTENER NODOS
    # ====================================================

    def _obtener_nodos(self, nodo):
        """
        Obtiene todos los nodos del árbol.
        """

        lista = []

        def recorrer(actual):

            if actual is None:
                return

            lista.append(actual)

            recorrer(actual.izquierda)
            recorrer(actual.derecha)

        recorrer(nodo)

        return lista

    # ====================================================
    # MOSTRAR ÁRBOL
    # ====================================================

    def mostrar_arbol(self):
        """
        Imprime el árbol de expresión en consola.

        Utiliza:

        /
        \

        para representar las conexiones.
        """

        print("\n" + "-" * 70)
        print("ÁRBOL DE EXPRESIÓN")
        print("-" * 70)

        if not self.raiz:

            print("Árbol vacío.")

            return

        posiciones = self._calcular_posiciones(
            self.raiz
        )

        nodos = self._obtener_nodos(
            self.raiz
        )

        # --------------------------------------------
        # AGRUPAR NODOS POR NIVEL
        # --------------------------------------------

        niveles = {}

        for actual in nodos:

            x, nivel = posiciones[id(actual)]

            if nivel not in niveles:
                niveles[nivel] = []

            niveles[nivel].append(actual)

        # --------------------------------------------
        # ORDENAR NODOS HORIZONTALMENTE
        # --------------------------------------------

        for nivel in niveles:

            niveles[nivel].sort(
                key=lambda nodo:
                posiciones[id(nodo)][0]
            )

        max_nivel = max(
            niveles.keys()
        )

        max_x = max(
            posicion[0]
            for posicion in posiciones.values()
        )

        # Espacio total de impresión
        ancho = max_x + 8

        # --------------------------------------------
        # IMPRIMIR CADA NIVEL
        # --------------------------------------------

        for nivel in range(max_nivel + 1):

            linea = [" "] * ancho

            # ----------------------------------------
            # NODOS
            # ----------------------------------------

            for actual in niveles.get(
                nivel,
                []
            ):

                x, _ = posiciones[
                    id(actual)
                ]

                valor = str(
                    actual.valor
                )

                inicio = (
                    x
                    - len(valor) // 2
                )

                for i, caracter in enumerate(
                    valor
                ):

                    posicion = inicio + i

                    if (
                        0 <= posicion < ancho
                    ):

                        linea[posicion] = caracter

            print(
                "".join(linea).rstrip()
            )

            # ----------------------------------------
            # RAMAS
            # ----------------------------------------

            if nivel < max_nivel:

                # Dos líneas para que las ramas
                # tengan una inclinación más clara.
                for fraccion in (
                    1 / 3,
                    2 / 3
                ):

                    linea_ramas = [
                        " "
                    ] * ancho

                    for actual in niveles.get(
                        nivel,
                        []
                    ):

                        x, _ = posiciones[
                            id(actual)
                        ]

                        # ----------------------------
                        # RAMA IZQUIERDA
                        # ----------------------------

                        if actual.izquierda:

                            x_hijo, _ = posiciones[
                                id(
                                    actual.izquierda
                                )
                            ]

                            punto = round(
                                x
                                + (
                                    x_hijo - x
                                )
                                * fraccion
                            )

                            if (
                                0
                                <= punto
                                < ancho
                            ):

                                linea_ramas[
                                    punto
                                ] = "/"

                        # ----------------------------
                        # RAMA DERECHA
                        # ----------------------------

                        if actual.derecha:

                            x_hijo, _ = posiciones[
                                id(
                                    actual.derecha
                                )
                            ]

                            punto = round(
                                x
                                + (
                                    x_hijo - x
                                )
                                * fraccion
                            )

                            if (
                                0
                                <= punto
                                < ancho
                            ):

                                linea_ramas[
                                    punto
                                ] = "\\"

                    print(
                        "".join(
                            linea_ramas
                        ).rstrip()
                    )