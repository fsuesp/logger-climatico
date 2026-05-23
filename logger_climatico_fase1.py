import requests
import csv
import os

class ConsultaClima:
    def __init__(self,api_key):
        
        self.api_key = api_key

    def obtener_clima(self,ciudad):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={self.api_key}&units=metric&lang=es"

        try:
            respuesta = requests.get(url)

            if respuesta.status_code == 200:
                datos = respuesta.json()

                return datos
            
            elif respuesta.status_code == 400:
                print("Ciudad no encontrada")
            
            else:
                print(f'ERROR: {respuesta.status_code}')

        except requests.exceptions.ConnectionError:
            print("No hay coneccion a internet")

class HistorialCSV:
    def __init__(self,nombre_archivo):
        self.nombre_archivo = nombre_archivo
    
    def historialclima(self,ciudad,temperatura,humedad,descripccion):
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo,"a",newline="") as file:
                escritor = csv.writer(file)
                escritor.writerow([ciudad,temperatura,humedad,descripccion])
        else:
            with open (self.nombre_archivo,"a",newline="") as file:
                escritor = csv.writer(file)
                escritor.writerow(["Ciudad","Temperatura","Humedad","descripccion"])
                escritor.writerow([ciudad,temperatura,humedad,descripccion])

    def mostrarhistorial(self):
        if os.path.exists(self.nombre_archivo):
            with open(self.nombre_archivo,"r") as file:
                lector = csv.DictReader(file)

                for fila in lector:
                    print(fila)
        
        else:
            print("El historial del clima esta vacio")



consultaclima = ConsultaClima("ef3cfa6e5dfd84252949ad0fbbe9d275")
historial = HistorialCSV("historial_clima.csv")

while True:

    print("---Estacion Climatica---\n")
    print("---Menu---\n")
    print("1-Mostrar clima")
    print("2-Ver Historial de Busqueda")
    print("0-Salir")

    try:
        op = int(input("Ingrese una opccion: "))

        if op < 0 or op > 2:
            print("Opccion invalida")
            continue
    except ValueError:
        print("Opccion Invalida")
        continue

    if op == 1:
        
        ciudad = input("Locacion: ")

        clima = consultaclima.obtener_clima(ciudad)
        if clima:
            ciudad_nombre = clima['name']
            temperatura = clima['main']['temp']
            humedad = clima['main']['humidity']
            descripcion = clima['weather'][0]['description']
    
            print(f"Ciudad: {ciudad_nombre}")
            print(f"Temperatura: {temperatura}°C")
            print(f"Humedad: {humedad}%")
            print(f"Descripción: {descripcion}")
            
            historial.historialclima(ciudad_nombre, temperatura, humedad, descripcion)

        
    if op == 2:
        historial.mostrarhistorial()
    
    if op == 0:
        print("Saliendo dle sistema...")
        break



        


