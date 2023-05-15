import requests
import time
import random

counter = 0

while True:
    data = {"Nodo": str(random.randint(0,9)), "sensorPH": str(random.randint(20,30)), "sensorTEMP": str(random.randint(100,320))}
    headers = {"Content-type": "application/json"}
    response = requests.post("http://127.0.0.1:5001/new_transaction", json=data, headers=headers)
    print(response.status_code)
    counter += 1
    if counter == 10:
        response = requests.get("http://127.0.0.1:5001/mine")
        print(response.status_code)
        counter = 0
        time.sleep(10)  # espera 5 segundos antes de enviar otra solicitud
    time.sleep(1) # espera 5 segundos antes de enviar otra solicitud