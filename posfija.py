from Notaciones import Utilidades

class posfija(Utilidades):
    """
    Clase encargada de la conversión de Notación Infija a Posfija.
    Hereda de Utilidades.
    """

    def convertir(self, tokens):
        salida = []
        pila = []
        pasos = []
        paso = 1

        for token in tokens:
            accion = ""

            # Operando
            if token.isalnum():
                salida.append(token)
                accion = "Mandar operando a salida"

            # Paréntesis izquierdo
            elif token == "(":
                pila.append(token)
                accion = "Meter '(' en la pila"

            # Paréntesis derecho
            elif token == ")":
                operadores = []
                while pila and pila[-1] != "(":
                    op = pila.pop()
                    salida.append(op)
                    operadores.append(op)

                if pila:
                    pila.pop()  # Eliminar '('

                if operadores:
                    accion = f"Sacar {', '.join(operadores)} de la pila"
                else:
                    accion = "Eliminar paréntesis"

            # Operador
            elif self.es_operador(token):
                operadores = []
                while (
                    pila
                    and self.es_operador(pila[-1])
                    and self.prioridad(pila[-1]) >= self.prioridad(token)
                ):
                    op = pila.pop()
                    salida.append(op)
                    operadores.append(op)

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
            op = pila.pop()
            salida.append(op)
            pasos.append({
                "paso": paso,
                "token": "FIN",
                "accion": f"Sacar {op} de la pila",
                "pila": pila.copy(),
                "salida": salida.copy(),
            })
            paso += 1

        return salida, pasos