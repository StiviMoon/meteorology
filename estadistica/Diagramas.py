

from estadistica.Funciones import ordenar_datos, calcular_mediana

def diagrama_frecuencia(datos):
    # Validaciones básicas
    if not datos:
        print("⚠️ No hay datos para graficar.")
        return
    
    for valor in datos:
        if not isinstance(valor, (int, float)):
            print("⚠️ Los datos deben ser numéricos.")
            return

    # Contar frecuencias
    valores = []
    frecuencias = []

    for valor in datos:
        if valor in valores:
            i = 0
            for v in valores:
                if v == valor:
                    frecuencias[i] += 1
                    break
                i += 1
        else:
            valores.append(valor)
            frecuencias.append(1)

    # Ordenar los valores (usando tu burbuja)
    for i in range(len(valores)):
        for j in range(len(valores) - 1 - i):
            if valores[j] > valores[j + 1]:
                temp = valores[j]
                valores[j] = valores[j + 1]
                valores[j + 1] = temp
                ftemp = frecuencias[j]
                frecuencias[j] = frecuencias[j + 1]
                frecuencias[j + 1] = ftemp

    # Mostrar histograma textual
    print("\n📊 DIAGRAMA DE FRECUENCIA")
    for i in range(len(valores)):
        barras = "*" * frecuencias[i]
        print(f"{valores[i]} | {barras} ({frecuencias[i]})")


def diagrama_caja(datos):
    if not datos:
        print("⚠️ No hay datos para graficar.")
        return

    datos_ordenados = ordenar_datos(datos)
    n = len(datos_ordenados)

    # Calcular Q1 y Q3
    mitad = n // 2
    # La mitad inferior es la misma tanto si n es par como impar
    mitad_inferior = datos_ordenados[:mitad]
    if n % 2 == 0:
        mitad_superior = datos_ordenados[mitad:]
    else:
        mitad_superior = datos_ordenados[mitad + 1:]

    q1 = calcular_mediana(mitad_inferior)
    q3 = calcular_mediana(mitad_superior)
    minimo = datos_ordenados[0]
    maximo = datos_ordenados[-1]

    # Calcular mediana general (mover más cerca de su uso)
    mediana = calcular_mediana(datos_ordenados)

    # Mostrar de forma textual
    print("\n📦 DIAGRAMA DE CAJA")
    print("Min  Q1  Q2  Q3  Max")
    print(f"{minimo}  {q1}  {mediana}  {q3}  {maximo}")
    print("|----|----|----|----|")
