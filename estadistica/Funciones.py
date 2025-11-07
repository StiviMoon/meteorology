# -------------------------------
# Módulo de Estadística Descriptiva
# -------------------------------
# Proyecto: Estación Meteorológica
# Sin librerías externas
# -------------------------------

# -------------------------------
# FUNCION: Calcular Media
# -------------------------------
def calcular_media(datos):
    # Validación: lista vacía
    if not datos:
        print("⚠️ Error: la lista de datos está vacía.")
        return None

    # Validación: tipos numéricos
    for valor in datos:
        if not isinstance(valor, (int, float)):
            print("⚠️ Error: todos los elementos deben ser numéricos.")
            return None

    # Calcular suma y cantidad
    suma = 0
    cantidad = 0
    for valor in datos:
        suma += valor
        cantidad += 1

    # Calcular media
    media = suma / cantidad
    return media


# -------------------------------
# FUNCION: Ordenamiento Burbuja
# -------------------------------
def ordenar_datos(datos):
    # Clonar lista original
    resultado = []
    for valor in datos:
        resultado.append(valor)

    # Contar elementos
    n = 0
    for _ in resultado:
        n += 1

    # Algoritmo de burbuja
    for i in range(n):
        for j in range(0, n - 1 - i):
            if resultado[j] > resultado[j + 1]:
                temp = resultado[j]
                resultado[j] = resultado[j + 1]
                resultado[j + 1] = temp

    return resultado


# -------------------------------
# FUNCION: Calcular Mediana
# -------------------------------
def calcular_mediana(datos):
    if not datos:
        print("⚠️ Error: la lista de datos está vacía.")
        return None

    for valor in datos:
        if not isinstance(valor, (int, float)):
            print("⚠️ Error: todos los elementos deben ser numéricos.")
            return None

    # Ordenar datos
    datos_ordenados = ordenar_datos(datos)

    # Contar elementos
    cantidad = 0
    for _ in datos_ordenados:
        cantidad += 1

    # Calcular índice central
    indice_central = cantidad // 2

    # Calcular mediana según par o impar
    if cantidad % 2 == 1:
        mediana = datos_ordenados[indice_central]
    else:
        valor1 = datos_ordenados[indice_central - 1]
        valor2 = datos_ordenados[indice_central]
        mediana = (valor1 + valor2) / 2

    return mediana


# -------------------------------
# FUNCION: Calcular Moda
# -------------------------------
def calcular_moda(datos):
    if not datos:
        print("⚠️ Error: la lista de datos está vacía.")
        return None

    for valor in datos:
        if not isinstance(valor, (int, float)):
            print("⚠️ Error: todos los elementos deben ser numéricos.")
            return None

    # PASO 1 — Contar frecuencias
    valores = []
    frecuencias = []

    for valor in datos:
        if valor in valores:
            indice = 0
            for v in valores:
                if v == valor:
                    frecuencias[indice] += 1
                    break
                indice += 1
        else:
            valores.append(valor)
            frecuencias.append(1)

    # PASO 2 — Frecuencia máxima
    frecuencia_max = frecuencias[0]
    for f in frecuencias:
        if f > frecuencia_max:
            frecuencia_max = f

    # PASO 3 — Verificar si hay moda
    if frecuencia_max == 1:
        return {
            "moda": [],
            "frecuencia": 1,
            "tipo": "sin_moda",
            "mensaje": "No hay moda (ningún valor se repite)"
        }

    # PASO 4 — Identificar valores con frecuencia máxima
    modales = []
    for i in range(len(valores)):
        if frecuencias[i] == frecuencia_max:
            modales.append(valores[i])

    # Ordenar modales (burbuja)
    modales_ordenados = ordenar_datos(modales)

    # PASO 5 — Clasificar tipo de moda
    cantidad_modas = 0
    for _ in modales_ordenados:
        cantidad_modas += 1

    if cantidad_modas == 1:
        tipo = "unimodal"
    elif cantidad_modas == 2:
        tipo = "bimodal"
    else:
        tipo = "multimodal"

    return {
        "moda": modales_ordenados,
        "frecuencia": frecuencia_max,
        "tipo": tipo
    }


# -------------------------------
# FUNCION: Calcular Varianza y Desviación Estándar
# -------------------------------
def calcular_varianza(datos, poblacional=False):
    if not datos:
        print("⚠️ Error: la lista de datos está vacía.")
        return None

    for valor in datos:
        if not isinstance(valor, (int, float)):
            print("⚠️ Error: todos los elementos deben ser numéricos.")
            return None

    # Calcular media
    media = calcular_media(datos)

    # Calcular sumatoria de desviaciones al cuadrado
    suma_cuadrados = 0
    cantidad = 0
    for valor in datos:
        desviacion = valor - media
        suma_cuadrados += desviacion * desviacion
        cantidad += 1

    if cantidad <= 1:
        print("⚠️ Error: no se puede calcular varianza con menos de 2 datos.")
        return None

    # Varianza poblacional o muestral
    divisor = cantidad if poblacional else (cantidad - 1)
    varianza = suma_cuadrados / divisor
    return varianza


def calcular_desviacion_estandar(datos, poblacional=False):
    varianza = calcular_varianza(datos, poblacional)
    if varianza is None:
        return None

    # Raíz cuadrada manual sin librerías
    # Método de Newton-Raphson
    estimacion = varianza / 2
    for _ in range(10):  # iteraciones suficientes
        estimacion = (estimacion + varianza / estimacion) / 2

    return estimacion


# -------------------------------
# PRUEBAS DE EJEMPLO
# -------------------------------
if __name__ == "__main__":
    datos = [2, 4, 4, 4, 5, 5, 7, 9]

    print("Datos:", datos)
    print("Media:", calcular_media(datos))
    print("Mediana:", calcular_mediana(datos))
    print("Moda:", calcular_moda(datos))
    print("Varianza:", calcular_varianza(datos))
    print("Desviación estándar:", calcular_desviacion_estandar(datos))
