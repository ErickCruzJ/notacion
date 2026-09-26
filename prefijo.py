
# ============================================================
# CONVERSOR DE EXPRESIONES INFIJAS A PREFIJAS
# ============================================================


# ============================================================
# 1. PRIORIDAD DE OPERADORES
# ============================================================

def prioridad(operador):

    if operador in ("+", "-"):
        return 1

    if operador in ("*", "/"):
        return 2

    if operador == "^":
        return 3

    return 0


# ============================================================
# 2. COMPROBAR SI ES OPERADOR
# ============================================================

def es_operador(caracter):

    return caracter in ("+", "-", "*", "/", "^")


# ============================================================
# 3. SEPARAR LA EXPRESIÓN EN TOKENS
# ============================================================

def tokenizar(expresion):

    tokens = []
    numero = ""

    for caracter in expresion:

        # Ignorar espacios
        if caracter == " ":
            continue

        # Si es un número
        if caracter.isdigit():

            numero += caracter

        else:

            # Guardar número antes del operador
            if numero:

                tokens.append(numero)
                numero = ""

            tokens.append(caracter)

    # Guardar último número
    if numero:

        tokens.append(numero)

    return tokens


# ============================================================
# 4. VALIDAR PARÉNTESIS
# ============================================================

def validar_parentesis(tokens):

    contador = 0

    for token in tokens:

        if token == "(":

            contador += 1

        elif token == ")":

            contador -= 1

            if contador < 0:

                return False

    return contador == 0


# ============================================================
# 5. CONVERTIR INFIJA A PREFIJA
# ============================================================

def convertir_prefijo(tokens):

    pila = []
    salida = []
    pasos = []

    # --------------------------------------------------------
    # Para obtener prefijo procesamos de derecha a izquierda
    # --------------------------------------------------------

    tokens_invertidos = tokens[::-1]

    paso = 1

    for token in tokens_invertidos:

        accion = ""

        # ====================================================
        # OPERANDO
        # ====================================================

        if token.isalnum():

            salida.append(token)

            accion = "Mandar operando a salida"

        # ====================================================
        # PARÉNTESIS DERECHO
        # ====================================================

        elif token == ")":

            pila.append(token)

            accion = "Meter ')' en la pila"

        # ====================================================
        # PARÉNTESIS IZQUIERDO
        # ====================================================

        elif token == "(":

            operadores = []

            while pila and pila[-1] != ")":

                operador = pila.pop()

                salida.append(operador)

                operadores.append(operador)

            # Eliminar ')'
            if pila:

                pila.pop()

            if operadores:

                accion = (
                    "Sacar "
                    + ", ".join(operadores)
                    + " de la pila"
                )

            else:

                accion = "Eliminar paréntesis"

        # ====================================================
        # OPERADOR
        # ====================================================

        elif es_operador(token):

            operadores = []

            while (
                pila
                and pila[-1] != ")"
                and prioridad(pila[-1]) > prioridad(token)
            ):

                operador = pila.pop()

                salida.append(operador)

                operadores.append(operador)

            pila.append(token)

            if operadores:

                accion = (
                    "Sacar "
                    + ", ".join(operadores)
                    + " y meter "
                    + token
                    + " en pila"
                )

            else:

                accion = (
                    "Meter "
                    + token
                    + " en pila"
                )

        # ====================================================
        # GUARDAR PASO
        # ====================================================

        pasos.append({
            "paso": paso,
            "token": token,
            "accion": accion,
            "pila": pila.copy(),
            "salida": salida.copy()
        })

        paso += 1

    # ========================================================
    # VACIAR PILA
    # ========================================================

    while pila:

        operador = pila.pop()

        salida.append(operador)

        pasos.append({
            "paso": paso,
            "token": "FIN",
            "accion": (
                "Sacar "
                + operador
                + " de la pila"
            ),
            "pila": pila.copy(),
            "salida": salida.copy()
        })

        paso += 1

    # ========================================================
    # INVERTIR SALIDA
    # ========================================================

    prefijo = salida[::-1]

    return prefijo, pasos


# ============================================================
# 6. MOSTRAR TABLA DEL PROCESO
# ============================================================

def mostrar_proceso(pasos):

    print()
    print("----------------------------------------")
    print("PROCESO")
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

        pila = " ".join(
            paso["pila"]
        )

        salida = " ".join(
            paso["salida"]
        )

        print(
            f"{paso['paso']:<6}"
            f"{paso['token']:<8}"
            f"{paso['accion']:<42}"
            f"{pila:<15}"
            f"{salida}"
        )


# ============================================================
# 7. NODO DEL ÁRBOL
# ============================================================

class Nodo:

    def __init__(self, valor):

        self.valor = valor
        self.izquierda = None
        self.derecha = None


# ============================================================
# 8. CONSTRUIR ÁRBOL DESDE PREFIJO
# ============================================================

def construir_arbol(prefijo):

    pila = []

    # --------------------------------------------------------
    # Recorrer prefijo de derecha a izquierda
    # --------------------------------------------------------

    for token in reversed(prefijo):

        # ----------------------------------------------------
        # OPERANDO
        # ----------------------------------------------------

        if token.isalnum():

            nodo = Nodo(token)

            pila.append(nodo)

        # ----------------------------------------------------
        # OPERADOR
        # ----------------------------------------------------

        elif es_operador(token):

            nodo = Nodo(token)

            # Primer elemento de la pila = izquierda
            nodo.izquierda = pila.pop()

            # Segundo elemento = derecha
            nodo.derecha = pila.pop()

            pila.append(nodo)

    return pila[0]


# ============================================================
# 9. ASIGNAR POSICIONES A LOS NODOS
# ============================================================

def calcular_posiciones(nodo):

    posiciones = {}

    contador = [0]

    def recorrer(actual, nivel):

        if actual is None:

            return

        # Primero izquierda
        recorrer(
            actual.izquierda,
            nivel + 1
        )

        # Si es hoja
        if (
            actual.izquierda is None
            and actual.derecha is None
        ):

            x = contador[0]

            contador[0] += 8

        # Si tiene dos hijos
        elif (
            actual.izquierda is not None
            and actual.derecha is not None
        ):

            x_izq = posiciones[
                id(actual.izquierda)
            ][0]

            # Primero procesamos derecha
            recorrer(
                actual.derecha,
                nivel + 1
            )

            x_der = posiciones[
                id(actual.derecha)
            ][0]

            x = (
                x_izq + x_der
            ) // 2

        # Solo derecha
        elif actual.derecha is not None:

            recorrer(
                actual.derecha,
                nivel + 1
            )

            x = posiciones[
                id(actual.derecha)
            ][0]

        # Solo izquierda
        else:

            x = posiciones[
                id(actual.izquierda)
            ][0]

        posiciones[
            id(actual)
        ] = (
            x,
            nivel
        )

    recorrer(nodo, 0)

    return posiciones


# ============================================================
# 10. OBTENER TODOS LOS NODOS
# ============================================================

def obtener_nodos(nodo):

    lista = []

    def recorrer(actual):

        if actual is None:

            return

        lista.append(actual)

        recorrer(actual.izquierda)
        recorrer(actual.derecha)

    recorrer(nodo)

    return lista


# ============================================================
# 11. MOSTRAR ÁRBOL VISUAL
# ============================================================

def mostrar_arbol(nodo):

    print()
    print("----------------------------------------")
    print("ÁRBOL DE EXPRESIÓN")
    print("----------------------------------------")

    posiciones = calcular_posiciones(nodo)

    nodos = obtener_nodos(nodo)

    # --------------------------------------------------------
    # Determinar altura
    # --------------------------------------------------------

    niveles = {}

    for actual in nodos:

        x, nivel = posiciones[
            id(actual)
        ]

        if nivel not in niveles:

            niveles[nivel] = []

        niveles[nivel].append(actual)

    max_nivel = max(
        niveles.keys()
    )

    # --------------------------------------------------------
    # Dibujar cada nivel
    # --------------------------------------------------------

    for nivel in range(
        max_nivel + 1
    ):

        # ====================================================
        # NODOS
        # ====================================================

        linea = [" "] * 100

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

                if (
                    0 <= inicio + i < len(linea)
                ):

                    linea[
                        inicio + i
                    ] = caracter

        print(
            "".join(linea).rstrip()
        )

        # ====================================================
        # RAMAS
        # ====================================================

        if nivel < max_nivel:

            linea_ramas = [" "] * 100

            for actual in niveles.get(
                nivel,
                []
            ):

                x, _ = posiciones[
                    id(actual)
                ]

                # --------------------------------------------
                # Rama izquierda
                # --------------------------------------------

                if actual.izquierda:

                    x_hijo, _ = posiciones[
                        id(actual.izquierda)
                    ]

                    punto = (
                        x + x_hijo
                    ) // 2

                    if (
                        0 <= punto < len(linea_ramas)
                    ):

                        linea_ramas[
                            punto
                        ] = "/"

                # --------------------------------------------
                # Rama derecha
                # --------------------------------------------

                if actual.derecha:

                    x_hijo, _ = posiciones[
                        id(actual.derecha)
                    ]

                    punto = (
                        x + x_hijo
                    ) // 2

                    if (
                        0 <= punto < len(linea_ramas)
                    ):

                        linea_ramas[
                            punto
                        ] = "\\"

            print(
                "".join(linea_ramas).rstrip()
            )


# ============================================================
# 12. RECORRIDO PREFIJO
# ============================================================

def recorrido_prefijo(nodo):

    recorrido = []

    def recorrer(actual):

        if actual is None:

            return

        # --------------------------------------------
        # 1. RAÍZ
        # --------------------------------------------

        recorrido.append(
            actual.valor
        )

        # --------------------------------------------
        # 2. IZQUIERDA
        # --------------------------------------------

        recorrer(
            actual.izquierda
        )

        # --------------------------------------------
        # 3. DERECHA
        # --------------------------------------------

        recorrer(
            actual.derecha
        )

    recorrer(nodo)

    return recorrido


# ============================================================
# 13. PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 50)
    print("       CONVERSOR DE EXPRESIONES")
    print("=" * 50)

    # --------------------------------------------------------
    # PEDIR EXPRESIÓN
    # --------------------------------------------------------

    expresion = input(
        "\nIntroduce una expresión:\n> "
    )

    # --------------------------------------------------------
    # TOKENIZAR
    # --------------------------------------------------------

    tokens = tokenizar(
        expresion
    )

    # --------------------------------------------------------
    # VALIDAR
    # --------------------------------------------------------

    if not validar_parentesis(tokens):

        print()
        print("ERROR:")
        print(
            "Los paréntesis no están balanceados."
        )

        return

    # --------------------------------------------------------
    # EXPRESIÓN INFIJA
    # --------------------------------------------------------

    print()
    print("----------------------------------------")
    print("EXPRESIÓN INFIJA")
    print("----------------------------------------")

    print(
        " ".join(tokens)
    )

    # --------------------------------------------------------
    # CONVERSIÓN
    # --------------------------------------------------------

    prefijo, pasos = convertir_prefijo(
        tokens
    )

    # --------------------------------------------------------
    # MOSTRAR PROCESO
    # --------------------------------------------------------

    mostrar_proceso(
        pasos
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print()
    print("----------------------------------------")
    print("RESULTADO PREFIJO")
    print("----------------------------------------")

    print(
        " ".join(prefijo)
    )

    # --------------------------------------------------------
    # CONSTRUIR ÁRBOL
    # --------------------------------------------------------

    arbol = construir_arbol(
        prefijo
    )

    # --------------------------------------------------------
    # MOSTRAR ÁRBOL
    # --------------------------------------------------------

    mostrar_arbol(
        arbol
    )

    # --------------------------------------------------------
    # RECORRIDO
    # --------------------------------------------------------

    recorrido = recorrido_prefijo(
        arbol
    )

    # --------------------------------------------------------
    # MOSTRAR RECORRIDO
    # --------------------------------------------------------

    print()
    print("----------------------------------------")
    print("RECORRIDO PREFIJO")
    print("----------------------------------------")

    print(
        " → ".join(recorrido)
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    main()

