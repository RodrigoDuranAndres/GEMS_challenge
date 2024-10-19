import requests
import json
import os

number = 1
with open(f"./example_payloads/payload{number}.json") as f:
    data = json.load(f)

url = 'http://localhost:8808/productionplan'
response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
data_list = json.loads(response.text)

ruta_archivo = f'./example_ouputs/response{number}.json'

# Si el archivo existe, bórralo
if os.path.exists(ruta_archivo):
    os.remove(ruta_archivo)

with open(ruta_archivo, 'w') as archivo:
    json.dump(data_list, archivo, indent=4)