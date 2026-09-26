def capturar_expresion(): #Función de captura una cadena
    expresion_texto = input("Ingresa la expresión: ")

    expresion_limpia = expresion_texto.replace(" ", "") #Limpiar los espacios en blanco

    tokens = [] #Convertimos la cadena limpia en una lista de caracteres individualizados
    for caracter in expresion_limpia: #Por cada caracter en la cadena
        tokens.append(caracter) #Agregar el caracter a la lista

    return tokens #Devolver la lista

def infija_a_posfija(tokens): #Función de infija a posfija requiere parametro lista
    salida = [] #Lista 
    pila_operadores = [] #Lista

    prioridad = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3} #Diccionario de prioridades

    for simbolo in tokens: #Por cada elemento de la lista
        
        if simbolo.isalnum(): #Si es una letra o número (operando) (Metodo nativo "is alpha-numeric" A-Z, a-z, 0-9)
            salida.append(simbolo) #Guardar en la lista salir

        elif simbolo == '(': #Si es un paréntesis que abre
            pila_operadores.append(simbolo) #Guardar en la lista pila_operadores

        elif simbolo == ')': #Si es un paréntesis que cierra
            while pila_operadores and pila_operadores[-1] != '(': #Mientras que la lista pila_operadores no este vacia y que el ultimo elemento no sea (
                salida.append(pila_operadores.pop()) #Se saca los elemento de la lista pila_operador y se agregan a la lista salida
            pila_operadores.pop()  #Eliminamos el ( de la lista pila_operacion

        elif simbolo in prioridad: #Si es un operador (+, -, *, /, ^)
            while (pila_operadores and pila_operadores[-1] in prioridad and prioridad[pila_operadores[-1]] >= prioridad[simbolo]): #Repetir si la pila_operadores tiene un operador (el ultimo guardado comparado en el diccionario) que ya está en la pila tiene mayor o igual prioridad que el nuevo operador que quiere agregar
                salida.append(pila_operadores.pop()) #Se saca los elemento de la lista pila_operador y se agregan a la lista salida
            pila_operadores.append(simbolo) #Se agrega en la lista pila_operadores el caracter

    while pila_operadores: #Vaciar los operadores restantes de la pila a la salida
        salida.append(pila_operadores.pop()) #Se saca los elemento de la lista pila_operador y se agregan a la lista salida

    return salida #Devolver la lista salida

if __name__ == "__main__":
    tokens = capturar_expresion()
    print("\nTokens Infijos:", tokens)

    #Conversiones directas
    posfija = infija_a_posfija(tokens)

    print("Notación Posfija (Postorden):", posfija)