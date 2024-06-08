import itertools
import sympy as sp
import os
import random


def find_numbers(n, X):
    numbers = set()
    max_attempts = 300
    attempts = 0
    while len(numbers) < n and attempts < max_attempts:
        attempts += 1
        num = random.randint(1, X - sum(numbers))
        if sum(numbers) + num <= X:
            numbers.add(num)
    return tuple(sorted(numbers))


def show_sums(numbers, suma_max):
    combinaciones = [c for c in itertools.combinations_with_replacement(numbers, len(numbers)) if sum(c) <= suma_max]
    aleatorios = []

    while len(aleatorios) < len(numbers) - 1:
        combinacion_aleatoria = random.choice(combinaciones)
        if combinacion_aleatoria not in aleatorios:
            aleatorios.append(combinacion_aleatoria)

    while True:
        combinacion_aleatoria = random.choice(combinaciones)
        temp_aleatorios = aleatorios.copy()
        temp_aleatorios.append(combinacion_aleatoria)

        all_numbers_present = all(any(number in aleatorio for aleatorio in temp_aleatorios) for number in numbers)

        if all_numbers_present:
            aleatorios.append(combinacion_aleatoria)
            break

    ecuaciones = [sp.Eq(sum(sp.Symbol(str(num)) for num in aleatorio), sum(aleatorio)) for aleatorio in aleatorios]

    sol = sp.solve(ecuaciones)

    return aleatorios, bool(sol)


def buscaItems(suma_max, num_of_incog):
    items = find_numbers(num_of_incog, suma_max)
    return items


def devuelve_sumas(suma_max, num_of_incog):
    intentos = 0
    max_intentos = 100
    sol_OK = False
    # print ("devuelve_sumas")
    while not sol_OK and intentos < max_intentos:
        try:

            numeros = ""
            i = 0
            while not(len(numeros) == num_of_incog):
                numeros = buscaItems(suma_max, num_of_incog)
                i +=1
                # print(i)
                # print(numeros)

            result, sol_OK = show_sums(numeros, suma_max)
            intentos += 1
        except ValueError as e:
            print(f"Se ha capturado un error: {e}")
            intentos += 1
        except:
            intentos += 1
            pass

    if sol_OK:
        return result
    else:
        print("No se encontró una solución en el límite de intentos.")
        return None




def convertir_numeros_a_imagenes(resultados, carpeta_imagenes):
    ruta = os.path.join("static", "img", "listado", carpeta_imagenes)
    imagenes_disponibles = os.listdir(ruta)

    if len(resultados) > len(imagenes_disponibles):
        raise ValueError("El número de resultados es mayor que el número de imágenes disponibles en la carpeta.")

    mapeo_numeros_imagenes = {}
    resultados_convertidos = []
    img_variables = []

    imagenes_usadas = random.sample(imagenes_disponibles, len(resultados))

    for resultado in resultados:
        resultado_convertido = []
        for num in resultado:
            if num not in mapeo_numeros_imagenes:
                imagen_asignada = "static/img/listado" + "/" + carpeta_imagenes + "/" + imagenes_usadas.pop(0)
                if imagen_asignada in img_variables:
                    raise ValueError("La imagen asignada ya existe en img_variables")
                mapeo_numeros_imagenes[num] = imagen_asignada
                img_variables.append(imagen_asignada)
            resultado_convertido.append(mapeo_numeros_imagenes[num])

        suma_total = sum(resultado)
        resultado_convertido.append(suma_total)
        resultados_convertidos.append(tuple(resultado_convertido))
    # print(img_variables)

    return resultados_convertidos, img_variables




def convertir_numeros_a_letras(resultados, carpeta_imagenes):
    letras = ['A', 'B', 'C', 'D', 'E']

    mapeo_numeros_letras = {}
    resultados_convertidos = []
    img_variables = []

    for resultado in resultados:
        resultado_convertido = []
        for num in resultado:
            if num not in mapeo_numeros_letras:
                mapeo_numeros_letras[num] = letras.pop(0)
            resultado_convertido.append(mapeo_numeros_letras[num])

        suma_total = sum(resultado)
        resultado_convertido.append(suma_total)
        resultados_convertidos.append(tuple(resultado_convertido))


    return resultados_convertidos

def devolver_variables(resultados):
    lista_sin_numeros = [elemento for elemento in resultados if not isinstance(elemento, int)]



    return lista_sin_numeros

def generar_ecuaciones(num_variables, suma_maxima, num_ejercicios, carpeta_imagenes):
    if num_variables > 5:
        raise ValueError(f"El número máximo de variables permitido es {num_variables}.")

    # Inicializa una lista vacía para almacenar los resultados de cada llamada a devuelve_sumas
    resultados = []
    incognitas = {}

    for i in range(num_ejercicios):
        l = devuelve_sumas(suma_maxima, num_variables)
        l, img_var = convertir_numeros_a_imagenes(l, carpeta_imagenes)

        resultados.append(l)
        incognitas[i] = img_var

    return resultados, incognitas

