from Notaciones import Utilidades

class prefija(Utilidades):
    """
    Clase encargada de la conversión de Notación Infija a Prefija.
    Hereda de Utilidades.
    """

    def convertir(self, tokens):
        pila = []
        salida = []
        pasos = []

        tokens_invertidos = tokens[::-1]
        paso = 1

        for token in tokens_invertidos:
            accion = ""

            # Operando
            if token.isalnum():
                salida.append(token)
                accion = "Mandar operando a salida"

            # Paréntesis derecho
            elif token == ")":
                pila.append(token)
                accion = "Meter ')' en la pila"

            # Paréntesis izquierdo
            elif token == "(":
                operadores = []
                while pila and pila[-1] != ")":
                    operador = pila.pop()
                    salida.append(operador)
                    operadores.append(operador)

                if pila:
                    pila.pop()  # Eliminar ')'

                if operadores:
                    accion = f"Sacar {', '.join(operadores)} de la pila"
                else:
                    accion = "Eliminar paréntesis"

            # Operador
            elif self.es_operador(token):
                operadores = []
                while (
                    pila
                    and pila[-1] != ")"
                    and self.prioridad(pila[-1]) > self.prioridad(token)
                ):
                    operador = pila.pop()
                    salida.append(operador)
                    operadores.append(operador)

                pila.append(token)

                if operadores:
                    accion = f"Sacar {', '.join(operadores)} y meter {token} en pila"
                else:
                    accion = f"Meter {token} en pila"

            pasos.append({
                "paso": paso,
                "token": token,
                "accion": accion,
                "pila": pila.copy(),
                "salida": salida.copy(),
            })
            paso += 1

        # Vaciar pila restante
        while pila:
            operador = pila.pop()
            salida.append(operador)
            pasos.append({
                "paso": paso,
                "token": "FIN",
                "accion": f"Sacar {operador} de la pila",
                "pila": pila.copy(),
                "salida": salida.copy(),
            })
            paso += 1

        prefijo = salida[::-1]
        return prefijo, pasos