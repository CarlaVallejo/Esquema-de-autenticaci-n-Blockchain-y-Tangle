import csv
import os
import time
import requests

filename1 = 'C:/Users/CARLA/Desktop/Red_IOTA/redIOTA1/data/tracking/node[0]Transaction1.csv'
filename2 = 'C:/Users/CARLA/Desktop/Red_IOTA/redIOTA1/data/tracking/node[0]Transaction2.csv'
filename3 = 'C:/Users/CARLA/Desktop/Red_IOTA/redIOTA1/data/tracking/node[0]Transaction3.csv'

transacciones = "http://192.168.0.104:5000/new_transaction"
minado = "http://192.168.0.104:5000/mine"

# Obtener la marca de tiempo inicial de los archivos
last_modified1 = os.path.getmtime(filename1)
last_modified2 = os.path.getmtime(filename2)
last_modified3 = os.path.getmtime(filename3)

while True:

    current_modified1 = os.path.getmtime(filename1)
    if current_modified1 != last_modified1:
        print("El archivo1 ha sido modificado")
        with open(filename1, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader)
            for row in reader:
                print(row)
                data = {"Nodo": row[0], "sensorPH": row[1],
                        "sensorTEMP": row[2]}
                headers = {"Content-type": "application/json"}
                response = requests.post(transacciones, json=data, headers=headers)
                print(response.status_code)

        last_modified1 = current_modified1

        response = requests.get(minado)
        print(response.status_code)
        print("El archivo1 ha sido minado")
        #time.sleep(2)


    current_modified2 = os.path.getmtime(filename2)
    if current_modified2 != last_modified2:
        print("El archivo2 ha sido modificado")
        # El archivo 2 ha sido modificado, así que leemos los nuevos datos
        with open(filename2, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader)  # Omitimos la primera fila que contiene los encabezados
            for row in reader:
                print(row)
                data = {"Nodo": row[0], "sensorPH": row[1],
                        "sensorTEMP": row[2]}  # Usamos los valores de la fila actual
                headers = {"Content-type": "application/json"}
                response = requests.post(transacciones, json=data, headers=headers)
                print(response.status_code)
                # Esperamos 1 segundo antes de enviar la siguiente solicitud POST

        # Actualizar la marca de tiempo del archivo 2
        last_modified2 = current_modified2

        # Enviar una solicitud GET después de enviar todas las solicitudes POST
        response = requests.get(minado)
        print(response.status_code)
        print("El archivo2 ha sido minado")
        #time.sleep(2)  # Esperar 10 segundos antes de enviar la siguiente solicitud GET

    current_modified3 = os.path.getmtime(filename3)
    if current_modified3 != last_modified3:
        print("El archivo3 ha sido modificado")
        # El archivo 3 ha sido modificado, así que leemos los nuevos datos
        with open(filename3, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader) # Omitimos la primera fila que contiene los encabezados
            for row in reader:
                print(row)
                data = {"Nodo": row[0], "sensorPH": row[1],
                "sensorTEMP": row[2]} # Usamos los valores de la fila actual
                headers = {"Content-type": "application/json"}
                response = requests.post(transacciones, json=data, headers=headers)
                print(response.status_code)
                # Esperamos 1 segundo antes de enviar la siguiente solicitud POST
        # Actualizar la marca de tiempo del archivo 3
        last_modified3 = current_modified3

        # Enviar una solicitud GET después de enviar todas las solicitudes POST
        response = requests.get(minado)
        print(response.status_code)
        print("El archivo3 ha sido minado")
        #time.sleep(2)  # Esperar 10 segundos antes de enviar la siguiente solicitud GET

    time.sleep(1)