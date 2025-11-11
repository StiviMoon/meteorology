# -------------------------------
# Módulo de Estadística Descriptiva
# -------------------------------
# Proyecto: Estación Meteorológica
# Sin librerías externas (solo Python nativo)
# -------------------------------

# -------------------------------
# FUNCION: Calcular Media
# -------------------------------
def calcular_media(datos):
    """Devuelve la media aritmética de una lista de números."""
    # Validación de datos numéricos
    datos_numericos = [x for x in datos if isinstance(x, (int, float))]
    if not datos_numericos:
        return None

    total = 0.0
    for x in datos_numericos:
        total += x

    return total / len(datos_numericos)


# -------------------------------
# FUNCION: Ordenamiento Burbuja
# -------------------------------
def ordenar_datos(datos):
    """Devuelve una nueva lista ordenada (burbuja)."""
    datos_copia = [x for x in datos if isinstance(x, (int, float))]
    n = len(datos_copia)

    for i in range(n - 1):
        for j in range(n - i - 1):
            if datos_copia[j] > datos_copia[j + 1]:
                datos_copia[j], datos_copia[j + 1] = datos_copia[j + 1], datos_copia[j]

    return datos_copia


# -------------------------------
# FUNCION: Calcular Mediana
# -------------------------------
def calcular_mediana(datos):
    """Devuelve la mediana de los datos."""
    datos_ordenados = ordenar_datos(datos)
    n = len(datos_ordenados)

    if n == 0:
        return None

    mitad = n // 2
    if n % 2 == 1:
        return datos_ordenados[mitad]
    else:
        return (datos_ordenados[mitad - 1] + datos_ordenados[mitad]) / 2


# -------------------------------
# FUNCION: Calcular Moda
# -------------------------------
def calcular_moda(datos):
    """Devuelve la moda o modas de una lista de números."""
    datos_numericos = [x for x in datos if isinstance(x, (int, float))]
    if not datos_numericos:
        return None

    # Contar frecuencias
    frecuencias = {}
    for x in datos_numericos:
        frecuencias[x] = frecuencias.get(x, 0) + 1

    # Frecuencia máxima
    max_frec = 0
    for f in frecuencias.values():
        if f > max_frec:
            max_frec = f

    # Sin moda (todos los valores aparecen una sola vez)
    if max_frec <= 1:
        return None

    modas = []
    for valor, frec in frecuencias.items():
        if frec == max_frec:
            modas.append(valor)

    modas_ordenadas = ordenar_datos(modas)
    return modas_ordenadas[0] if len(modas_ordenadas) == 1 else modas_ordenadas


# -------------------------------
# FUNCION: Calcular Varianza (Poblacional)
# -------------------------------
def calcular_varianza(datos):
    """Devuelve la varianza poblacional de los datos."""
    datos_numericos = [x for x in datos if isinstance(x, (int, float))]
    n = len(datos_numericos)
    if n == 0:
        return None

    media = calcular_media(datos_numericos)
    suma = 0.0
    for x in datos_numericos:
        suma += (x - media) ** 2

    return suma / n


# -------------------------------
# FUNCION: Calcular Desviación Estándar (Poblacional)
# -------------------------------
def calcular_std_dev(datos):
    """Devuelve la desviación estándar poblacional."""
    varianza = calcular_varianza(datos)
    if varianza is None:
        return None
    return varianza ** 0.5


# -------------------------------
# FUNCION: Calcular Rango Intercuartílico (IQR)
# -------------------------------
def calcular_iqr(datos):
    """Devuelve el rango intercuartílico (Q3 - Q1)."""
    datos_ordenados = ordenar_datos(datos)
    n = len(datos_ordenados)
    if n < 4:
        return None

    mitad = n // 2
    if n % 2 == 0:
        inferior = datos_ordenados[:mitad]
        superior = datos_ordenados[mitad:]
    else:
        inferior = datos_ordenados[:mitad]
        superior = datos_ordenados[mitad + 1:]

    q1 = calcular_mediana(inferior)
    q3 = calcular_mediana(superior)

    if q1 is None or q3 is None:
        return None

    return q3 - q1
# -------------------------------