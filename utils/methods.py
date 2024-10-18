from utils.clases import *
# from clases import *
# import numpy as np
# from scipy.optimize import linprog

def procesar_json(data):
    objevtive, plants = leer_json(data)
    # respuesta = usando_simplex_existe(objevtive, plants)
    # print("Simplex")
    # print(respuesta)
    respuesta = calcular_mejor_combinacion(objevtive, plants)
    print("Manual 1")
    print(respuesta)
    
    
    return respuesta

# def usando_simplex_existe(load, plants):
#     c = np.array([planta.precio_unidad_energia for planta in plants])
#     a_ub = np.eye(len(plants))
#     b_ub = np.array([planta.pmax for planta in plants])
#     
#     a_eq = np.ones(len(plants))
#     a_eq = a_eq.reshape(1, -1)
#     b_eq = np.array([load])
#     
#     res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=(0, None))
#     
#     respuesta_float = [float(respuesta) for respuesta in res.x]
#     nombre_plantas = [planta.nombre for planta in plants]
#     diccionarios = [{'name': x, 'p': y} for x, y in zip(nombre_plantas, respuesta_float)]
#     
#     return diccionarios

def planta_precio_menor(plants: list) -> PlantaEnergia:
    plantas_ordenadas = sorted(plants, key=lambda planta: planta.precio_unidad_energia)
    for planta in plantas_ordenadas:
        if planta.carga < planta.pmax:
            return planta
    return None

def planta_precio_menor_anterior(plants: list) -> PlantaEnergia:
    plantas_ordenadas = sorted(plants, key=lambda planta: planta.precio_unidad_energia)
    
    contador = 0
    while contador <= len(plantas_ordenadas):
        if plantas_ordenadas[contador].carga != plantas_ordenadas[contador].pmax:
            if contador - 1 < 0:
                return None
            else:
                return plantas_ordenadas[contador - 1]
        contador += 1
    return None

def planta_precio_minimo_menor(plants: list) -> PlantaEnergia:
    plantas_ordenadas = sorted(plants, key=lambda planta: planta.precio_minimo_activa)
    for planta in plantas_ordenadas:
        if planta.carga < planta.pmin:
            return planta
    return None

def calcular_mejor_combinacion(load_inicial: float, plants: list) -> list:
    diferencia = load_inicial

    while diferencia > 0:
        planta_menor = planta_precio_menor(plants)
        if planta_menor is None:
            break
        
        if diferencia >= (planta_menor.pmax - planta_menor.carga):
            planta_menor.write_carga(planta_menor.pmax)
        
        elif diferencia >= planta_menor.pmin:
            planta_menor.write_carga(diferencia + planta_menor.carga)
            
        else:
            planta_anterior = planta_precio_menor_anterior(plants)
            planta_activar = planta_precio_minimo_menor(plants)
            
            if planta_anterior is None:
                planta_menor.write_carga( planta_menor.min)
            
            if planta_anterior.pmax - planta_anterior.pmin > planta_menor.pmin:
                planta_menor.write_carga(planta_menor.pmin)
                planta_anterior.write_carga(planta_anterior.pmax - planta_menor.pmin + diferencia)
            else:
                planta_anterior.write_carga(0)
                planta_activar.write_carga(planta_activar.pmin)
                
        diferencia = load_inicial - sum([planta.carga for planta in plants])


    respuesta_float = [planta.carga for planta in plants]
    nombre_plantas = [planta.nombre for planta in plants]
    diccionarios = [{'name': x, 'p': y} for x, y in zip(nombre_plantas, respuesta_float)]
    
    return diccionarios
    


def leer_json(data):
    load = data["load"]
    fuels = data["fuels"]
    powerplants = data["powerplants"]
    
    velocidad_viento = fuels["wind(%)"] / 100
    precio_gas = fuels["gas(euro/MWh)"]
    precio_kerosine = fuels["kerosine(euro/MWh)"]
    precio_co2 = fuels["co2(euro/ton)"]
    
    instancias = []
    for planta in powerplants:
        if planta['type'] == 'windturbine':
            instancia = PlantaEnergia(planta['name'], planta['type'], planta['efficiency'], planta['pmin'], planta['pmax'] * velocidad_viento, 0)
        elif planta['type'] == 'gasfired':
            instancia = PlantaEnergia(planta['name'], planta['type'], planta['efficiency'], planta['pmin'], planta['pmax'], precio_gas)
        elif planta['type'] == 'turbojet':
            instancia = PlantaEnergia(planta['name'], planta['type'], planta['efficiency'], planta['pmin'], planta['pmax'], precio_kerosine)
        else:
            print("Error: Tipo de planta no válida")
        instancias.append(instancia)
    
    return load, instancias


#import json
#if __name__ == "__main__":
#    
#    with open("./example_payloads/payload3.json") as f:
#        data = json.load(f)
#    
#    procesar_json(data)