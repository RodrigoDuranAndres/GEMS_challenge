from utils.clases import *
import itertools
# from clases import *

def process_json(data):
    objective, plants = read_json(data)
    response = best_combination(objective, plants)
    diccionary = proces_response(response, plants)

    return diccionary

def proces_response(response, plants):
    for plant, load in response.items():
        plant.load = load

    response_float = [plant.load for plant in plants]
    name_plants = [plant.name for plant in plants]
    diccionary = [{'name': x, 'p': y} for x, y in zip(name_plants, response_float)]
    
    return diccionary

def best_combination(load_inicial: float, plants: list) -> list:
    plants_with_pmin_not_zero = [plant for plant in plants if plant.pmin != 0]
    plants_with_pmin_zero = [plant for plant in plants if plant.pmin== 0]
        
    best_status = 0; best_plants = []; best_cost = -1
    for r in range(len(plants_with_pmin_not_zero) + 1):
        for combination in itertools.combinations(plants_with_pmin_not_zero, r):
            subconjunto = list(combination) + plants_with_pmin_zero
            
            status, cost, plants = best_solution_plants(load_inicial, subconjunto)
            
            if status != -1 and (best_cost > cost or best_cost == -1):
                best_cost = cost
                best_plants = plants
                best_status = status
    
    return best_plants
    
def best_solution_plants(load_inicial: float, plants: list):
    if len(plants) == 0:
        return -1, None, None
    
    sum_plants_maximun = sum([plant.pmax for plant in plants])
    if sum_plants_maximun < load_inicial:
        return -1, None, None
    
    load = load_inicial
    plants_load = {plant: plant.pmin for plant in plants}
    sum_plants_minimun = sum([plant.pmin for plant in plants])
    plants_sorted = sorted(plants, key=lambda plant: plant.price_energy_unit)
    load -= sum_plants_minimun
    
    while load > 0:
        plant = plants_sorted.pop(0)
        if plants_load[plant] + load < plant.pmax:
            plants_load[plant] += load
            load = 0
        else:
            load -= (plant.pmax - plants_load[plant])
            plants_load[plant] = plant.pmax
            
    costo_total = 0
    for plant in plants:
        costo_total += plant.price_energy_unit * plants_load[plant]

    if load < 0:
        return -1, costo_total, plants_load
    else:
        return 0, costo_total, plants_load
    

def read_json(data):
    load = data["load"]
    fuels = data["fuels"]
    Powerplants = data["powerplants"]
    
    velocidad_viento = fuels["wind(%)"] / 100
    price_gas = fuels["gas(euro/MWh)"]
    price_kerosine = fuels["kerosine(euro/MWh)"]
    price_co2 = fuels["co2(euro/ton)"]
    
    instancias = []
    for plant in Powerplants:
        if plant['type'] == 'windturbine':
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'] * velocidad_viento)
        elif plant['type'] == 'gasfired':
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_gas, price_co2 = price_co2)
        elif plant['type'] == 'turbojet':
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_kerosine)
        else:
            raise ValueError(f"Unknown Powerplant type: {plant['type']}")
        instancias.append(instancia)
    
    return load, instancias


# import json
# if __name__ == "__main__":
#     
#     with open("./example_payloads/payload1.json") as f:
#         data = json.load(f)
#     
#     process_json(data)