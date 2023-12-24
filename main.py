import itertools
import random
import sympy as sp


def find_numbers(n, X):
    numbers = set()  # creamos un conjunto vacío para almacenar los números generados
    max_attempts = 100
    attempts = 0
    while len(numbers) < n:
        if attempts >= max_attempts:
            break
        attempts += 1
        num = random.randint(1, X - sum(numbers))  # genera un número aleatorio que no exceda la diferencia entre X y la suma de los números generados anteriormente
        if sum(numbers) + num > X:  # verifica si la suma de los números generados más el número actual excede X
            continue  # si excede, continuamos con la siguiente iteración del bucle sin agregar el número actual al conjunto
        numbers.add(num)  # agrega el número al conjunto
    # print(numbers)
    return tuple(sorted(numbers))  # convierte el conjunto en una tupla ordenada y la devuelve


# Definimos una función para mostrar las combinatorias de sumas
def show_sums(numbers, suma_max):
    combinaciones = [c for c in itertools.combinations_with_replacement(numbers, len(numbers)) if sum(c) <= suma_max]
    aleatorios = []

    for num in numbers:
        combinaciones_con_num = [c for c in combinaciones if num in c]
        combinacion_aleatoria = random.choice(combinaciones_con_num)

        # Revisa si la combinación aleatoria ya está en aleatorios
        while combinacion_aleatoria in aleatorios:
            combinaciones_con_num.remove(combinacion_aleatoria)  # Elimina la combinación duplicada de la lista
            if combinaciones_con_num:
                combinacion_aleatoria = random.choice(combinaciones_con_num)
            else:
                break

        aleatorios.append(combinacion_aleatoria)

    # print("Aleatorios:", aleatorios)

    ecuaciones = [sp.Eq(sum(sp.Symbol(str(num)) for num in aleatorio), sum(aleatorio)) for aleatorio in aleatorios]

    # Imprime las ecuaciones
    # for i, ecuacion in enumerate(ecuaciones, start=1):
    #    print(f"eq{i}: {ecuacion}")

    # Resuelve el sistema de ecuaciones usando la función solve()
    sol = sp.solve(ecuaciones)

    # print(sol)
    return aleatorios, bool(sol)


def buscaItems(suma_max,  num_of_incog):
    while True:
        try:
            items = find_numbers(num_of_incog, suma_max)
            break  # si la llamada a la función tiene éxito, salimos del bucle while
        except:
            pass  # si se genera una excepción, continuamos con la siguiente iteración del bucle while
    return items


def devuelve_sumas(suma_max, num_of_incog):
    intentos = 0
    max_intentos = 100
    sol_OK = False

    while not sol_OK and intentos < max_intentos:
        try:
            numeros = buscaItems(suma_max, num_of_incog)
            result, sol_OK = show_sums(numeros, suma_max)
            intentos += 1
        except:
            intentos += 1
            pass

    if sol_OK:
        # print("Resultado:")
        return result
    else:
        print("No se encontró una solución en el límite de intentos.")
        return None


def generar_ecuaciones(num_variables, suma_maxima, num_ejercicios):
    if num_variables > 5:
        raise ValueError(f"El número máximo de variables permitido es {num_variables}.")

    # Inicializa una lista vacía para almacenar los resultados de cada llamada a devuelve_sumas
    resultados = []

    for _ in range(num_ejercicios):
        l = devuelve_sumas(suma_maxima, num_variables)
        resultados.append(l)
        # print(l)

    return resultados

s = generar_ecuaciones(3, 30, 4)
print(s)