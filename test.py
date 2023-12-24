import itertools
import random
import sympy as sp

def find_numbers(n, X):
    numbers = set()
    while len(numbers) < n:
        num = random.randint(1, X - sum(numbers))
        if sum(numbers) + num > X:
            continue
        numbers.add(num)
    return tuple(sorted(numbers))

def combinaciones_posibles(numbers, n, suma_max):
    return [c for c in itertools.combinations_with_replacement(numbers, n) if sum(c) <= suma_max]

def selecciona_aleatorios(numbers, n):
    aleatorios = []
    for num in numbers:
        combinaciones = combinaciones_posibles(numbers, n, num)
        aleatorios.append(random.choice(combinaciones))
    return aleatorios

def crea_ecuaciones(aleatorios):
    ecuaciones = []
    for combinacion in aleatorios:
        ecuacion = sum([sp.Symbol(str(num)) for num in combinacion]) - sum(combinacion)
        ecuaciones.append(ecuacion)
    return ecuaciones

def buscaItems(suma_max):
    while True:
        try:
            print("buscar")
            items = find_numbers(3, suma_max)
            break
        except:
            print("BUSCAR K.O.")
            pass
    return items

def devulve_sumas(suma_max):
    intentos = 0
    max_intentos = 100

    while intentos < max_intentos:
        try:
            print("loop")
            numeros = buscaItems(suma_max)
            aleatorios = selecciona_aleatorios(numeros, 3)
            ecuaciones = crea_ecuaciones(aleatorios)
            sol = sp.solve(ecuaciones)
            sol_OK = bool(sol)

            if sol_OK:
                break
        except:
            print("error")

            pass

        intentos += 1

    if intentos < max_intentos:
        return aleatorios
    else:
        return None

resultado = devulve_sumas(30)
print("Resultado:")
print(resultado)
