import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics

def read_csv(archivo):
    data = {} 
    with open(archivo, 'r') as csvfile: #abrir csv modo lectura
        reader = csv.reader(csvfile) 
        headers = next(reader)# sacamos los encabezados del conjunto de datos
        
        for row in reader: #iteramos por filas
            period = row[0] 
            for i in range(1, len(headers)): #Iteramos para los 7 campos de marcas
                marca = headers[i]       
                valor = float(row[i])
                if marca not in data:  #verificar que la marca no este en data
                    data[marca] = {}   #crea un dict para esa marca
                data[marca][period] = valor  #almaceno en dict anidado, key ppal marca, key secundaria periodo
    
    return data



def calculate_statistics(data): #argumento data
    estadisticos_data = {}
       
    for marca, valores in data.items():
        ventas = np.array(list(valores.values())) #Array con numpy de los valores de ventas
        estadisticos_data[marca] = {   #añadimos los estadisticos al diccionario cuya key es la marca, dict anidado
            'Promedio': np.mean(ventas),
            'Mediana': np.median(ventas),           
            'std_dev': np.std(ventas),
            'min': np.min(ventas),
            'max': np.max(ventas)
        }
    return estadisticos_data #retorna el diccionario anidado


def grafico_barras_apiladas(data, ax):
    años = ['2018', '2019', '2020']
    marcas = list(data.keys()) #traigo solo las keys de data
    #Saco el total de ventas de cada marca en cada uno de los años    
    marca_ventas = {marca: [data[marca][f"{anio}Q1"] + data[marca][f"{anio}Q2"] + data[marca][f"{anio}Q3"] + data[marca][f"{anio}Q4"] for anio in años] for marca in marcas}
       
    colores = ['tab:blue', 'tab:orange', 'tab:green']
    
    bottom = np.zeros(len(marcas)) #array de ceros para el apilado
    
    for i, anio in enumerate(años):
        values = [marca_ventas[marca][i] for marca in marcas] #Extraemos el valor a gráficar de acuerdo a la marca y el año
        ax.bar(marcas, values, bottom=bottom, label=anio, color=colores[i])
        bottom = np.add(bottom, values) #Sumamos los valores al bottom para determinar donde inicia la siguiente barra apilada
    
    ax.set_xlabel('Marcas')
    ax.set_ylabel('Ventas')
    ax.set_title('Ventas totales por año')
    ax.legend(title='Año')
    ax.set_xticklabels(marcas, rotation=45)

def grafico_barras_prom(data, ax):
    marcas = list(data.keys())
    prom_ventas = [sum(data[marca].values()) / len(data[marca]) for marca in marcas] #extraemos valores de ventas totales, se suman y se dividen entre el numero de datos para el promedio
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink'] #colores de las barras
    
    ax.bar(marcas, prom_ventas, color=colors)
    ax.set_xlabel('Marca')
    ax.set_ylabel('Promedio de ventas')
    ax.set_title('Promedio de ventas por compañia (Histórico)')
    ax.set_xticklabels(marcas, rotation=45)

def grafico_cajas_bigotes(data):
    marcas = list(data.keys())
    datos_ventas = [list(data[marca].values()) for marca in marcas]# datos de ventas para cada marca
    
    fig, ax = plt.subplots() 
    ax.boxplot(datos_ventas, vert=False) #caja y bigotes horizontal
    ax.set_yticklabels(marcas)
    ax.set_xlabel('Ventas')
    ax.set_title('Distribución de ventas por marca')
    
    plt.show()

if __name__ == '__main__':
    archivo = 'smartphones.csv'  # nombre del archivo
    data = read_csv(archivo)
    
    estadisticos_data = calculate_statistics(data)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6)) #dos gráficos en la misma ventana
    
    grafico_barras_apiladas(data, axes[0])
    grafico_barras_prom(data, axes[1])
    
    plt.tight_layout() #ajustado a la ventana
    plt.show()
    
    grafico_cajas_bigotes(data)
    
    # imprimir los estadisticos calculados
    for marca, stats in estadisticos_data.items():
        print(f"{marca}:")
        print(f"  Promedio: {stats['Promedio']:.2f}")
        print(f"  Mediana: {stats['Mediana']}")
        print(f"  Desviación estandar: {stats['std_dev']:.2f}")
        print(f"  Min: {stats['min']}")
        print(f"  Max: {stats['max']}\n")
