import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from datetime import datetime
from conexion import conectar
# Configuración de la conexión a la base de datos
if conectar() is None :
    print("Error al conectar a la base de datos.")
    exit()
    
def obtener_datos():
    conexion = conectar()
    if not conexion:
        return [], []

    try:
        # Obtener datos de la base de datos
        cursor = conexion.cursor()
        # Ejecutar la consulta para obtener los datos de humedad
        cursor.execute("SELECT fecha_hora, humedad_porcentaje FROM humedad_datos ORDER BY fecha_hora ASC")
        # Mostrar los resultados de la consulta
        resultados = cursor.fetchall()
        # Las horas y porcentajes se almacenan en listas 
        # La linea dato[0] es la fecha y hora, y dato[1] es el porcentaje de humedad
        # Utilizamos strftime para formatear la fecha y hora y '%H:%M' para mostrar solo la hora y minuto
        horas = [dato[0].strftime('%H:%M') for dato in resultados]
        porcentajes = [dato[1] for dato in resultados]
        # Devolvemos las listas de horas y porcentajes
        return horas, porcentajes
    except Error as e:
        print("Error al obtener datos:", e)
        return [], []
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
# Esta funcion se crea una sola vez al inicio del programa y muestra los datos una vez obtenidos
def graficar(horas, porcentajes):
    plt.figure(figsize=(10, 5))
    plt.plot(horas, porcentajes, linestyle='--', color='red', marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Hora")
    plt.ylabel("Humedad (%)")
    plt.title("Humedad por Hora")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    horas, porcentajes = obtener_datos()
    if horas and porcentajes:
        graficar(horas, porcentajes)
    else:
        print("No hay datos para graficar.")