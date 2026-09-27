from Notaciones import Utilidades
from posfija import posfija

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolExpresion:
    """
    Gestiona la construcción, recorridos y representación visual del Árbol Sintáctico.
    """

    def __init__(self):
        self.raiz = None

    # ----------------------------------------------------
    # MÉTODOS DE CONSTRUCCIÓN
    # ----------------------------------------------------

    def construir_desde_prefija(self, tokens_prefijo):
        """Construye el árbol recorriendo tokens prefijos de derecha a izquierda."""
        pila = []

        for token in reversed(tokens_prefijo):
            if token.isalnum():
                nodo = Nodo(token)
                pila.append(nodo)
            elif Utilidades.es_operador(token):
                nodo = Nodo(token)
                if pila:
                    nodo.izquierda = pila.pop()
                if pila:
                    nodo.derecha = pila.pop()
                pila.append(nodo)

        self.raiz = pila[0] if pila else None
        return self.raiz

    def construir_desde_posfija(self, tokens_posfijo):
        """Construye el árbol recorriendo tokens posfijos de izquierda a derecha."""
        pila = []

        for token in tokens_posfijo:
            if token.isalnum():
                nodo = Nodo(token)
                pila.append(nodo)
            elif Utilidades.es_operador(token):
                nodo = Nodo(token)
                if pila:
                    nodo.derecha = pila.pop()
                if pila:
                    nodo.izquierda = pila.pop()
                pila.append(nodo)

        self.raiz = pila[0] if pila else None
        return self.raiz

    def construir_desde_infija(self, tokens_infijo):
        """
        Construye el árbol de expresión directamente a partir de la notación infija
        sin depender de las conversiones a posfija ni prefija.
        """
        pila_operandos = []  # Almacena objetos Nodo / Subárboles
        pila_operadores = [] # Almacena tokens de operadores y '('

        def procesar_operador():
            """Saca un operador y dos operandos para formar un subárbol."""
            if len(pila_operadores) > 0 and len(pila_operandos) >= 2:
                op_token = pila_operadores.pop()
                nodo_op = Nodo(op_token)
                
                # El segundo en salir es el hijo izquierdo, el primero es el derecho
                nodo_op.derecha = pila_operandos.pop()
                nodo_op.izquierda = pila_operandos.pop()
                
                # El nuevo subárbol vuelve a la pila de operandos
                pila_operandos.append(nodo_op)

        for token in tokens_infijo:
            # 1. Si es operando (letra o número)
            if token.isalnum():
                pila_operandos.append(Nodo(token))

            # 2. Si es paréntesis de apertura
            elif token == "(":
                pila_operadores.append(token)

            # 3. Si es paréntesis de cierre
            elif token == ")":
                while pila_operadores and pila_operadores[-1] != "(":
                    procesar_operador()
                if pila_operadores:
                    pila_operadores.pop()  # Eliminar '('

            # 4. Si es operador
            elif Utilidades.es_operador(token):
                while (
                    pila_operadores
                    and pila_operadores[-1] != "("
                    and Utilidades.prioridad(pila_operadores[-1]) >= Utilidades.prioridad(token)
                ):
                    procesar_operador()
                pila_operadores.append(token)

        # Vaciar los operadores restantes en la pila
        while pila_operadores:
            procesar_operador()

        # La raíz del árbol completo queda al final en la pila de operandos
        self.raiz = pila_operandos[0] if pila_operandos else None
        return self.raiz

    # ----------------------------------------------------
    # RECORRIDOS DEL ÁRBOL
    # ----------------------------------------------------

    def recorrido_infijo(self, nodo=None):
        """Inorden: Izquierda -> Raíz -> Derecha (sin paréntesis)."""
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

    def recorrido_prefijo(self, nodo=None):
        """Preorden: Raíz -> Izquierda -> Derecha."""
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

    def recorrido_posfijo(self, nodo=None):
        """Postorden: Izquierda -> Derecha -> Raíz."""
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

    # ----------------------------------------------------
    # DIBUJADO/VISUALIZACIÓN DEL ÁRBOL EN CONSOLA
    # ----------------------------------------------------

    def _calcular_posiciones(self, nodo):
        posiciones = {}
        contador = [0]

        def recorrer(actual, nivel):
            if actual is None:
                return

            recorrer(actual.izquierda, nivel + 1)

            if actual.izquierda is None and actual.derecha is None:
                x = contador[0]
                contador[0] += 8
            elif actual.izquierda is not None and actual.derecha is not None:
                x_izq = posiciones[id(actual.izquierda)][0]
                recorrer(actual.derecha, nivel + 1)
                x_der = posiciones[id(actual.derecha)][0]
                x = (x_izq + x_der) // 2
            elif actual.derecha is not None:
                recorrer(actual.derecha, nivel + 1)
                x = posiciones[id(actual.derecha)][0]
            else:
                x = posiciones[id(actual.izquierda)][0]

            posiciones[id(actual)] = (x, nivel)

        recorrer(nodo, 0)
        return posiciones

    def _obtener_nodos(self, nodo):
        lista = []

        def recorrer(actual):
            if actual is None:
                return
            lista.append(actual)
            recorrer(actual.izquierda)
            recorrer(actual.derecha)

        recorrer(nodo)
        return lista

    def mostrar_arbol(self):
        """Imprime la estructura jerárquica del árbol en consola."""
        print("\n----------------------------------------")
        print("ÁRBOL DE EXPRESIÓN")
        print("----------------------------------------")

        if not self.raiz:
            print("Árbol vacío.")
            return

        posiciones = self._calcular_posiciones(self.raiz)
        nodos = self._obtener_nodos(self.raiz)

        niveles = {}
        for actual in nodos:
            _, nivel = posiciones[id(actual)]
            if nivel not in niveles:
                niveles[nivel] = []
            niveles[nivel].append(actual)

        max_nivel = max(niveles.keys())

        for nivel in range(max_nivel + 1):
            linea = [" "] * 100
            for actual in niveles.get(nivel, []):
                x, _ = posiciones[id(actual)]
                valor = str(actual.valor)
                inicio = x - len(valor) // 2
                for i, caracter in enumerate(valor):
                    if 0 <= inicio + i < len(linea):
                        linea[inicio + i] = caracter

            print("".join(linea).rstrip())

            if nivel < max_nivel:
                linea_ramas = [" "] * 100
                for actual in niveles.get(nivel, []):
                    x, _ = posiciones[id(actual)]

                    if actual.izquierda:
                        x_hijo, _ = posiciones[id(actual.izquierda)]
                        punto = (x + x_hijo) // 2
                        if 0 <= punto < len(linea_ramas):
                            linea_ramas[punto] = "/"

                    if actual.derecha:
                        x_hijo, _ = posiciones[id(actual.derecha)]
                        punto = (x + x_hijo) // 2
                        if 0 <= punto < len(linea_ramas):
                            linea_ramas[punto] = "\\"

                print("".join(linea_ramas).rstrip())