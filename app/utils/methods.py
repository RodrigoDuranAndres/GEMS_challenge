from utils.clases import *
# from clases import *
# import numpy as np
# from scipy.optimize import linprog

def process_json(data):
    objective, plants = read_json(data)
    # response = use_simplex(objective, plants)
    # print("Simplex")
    # print(response)
    response = best_conbination(objective, plants)
    print("HandMade 1")
    print(response)
    
    return response

# def use_simplex(load, plants):
#     c = np.array([plant.price_energy_unit for plant in plants])
#     a_ub = np.eye(len(plants))
#     b_ub = np.array([plant.pmax for plant in plants])
#     
#     a_eq = np.ones(len(plants))
#     a_eq = a_eq.reshape(1, -1)
#     b_eq = np.array([load])
#     
#     res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=(0, None))
#     
#     response_float = [float(response) for response in res.x]
#     name_plants = [plant.name for plant in plants]
#     diccionary = [{'name': x, 'p': y} for x, y in zip(name_plants, response_float)]
#     
#     return diccionary

def plant_most_efficient(plants: list) -> Powerplant:
    plants_sorted = sorted(plants, key=lambda plant: plant.price_energy_unit)
    for plant in plants_sorted:
        if plant.load < plant.pmax:
            return plant
    return None

def plant_most_efficient_previous(plants: list) -> Powerplant:
    plants_sorted = sorted(plants, key=lambda plant: plant.price_energy_unit)
    
    count = 0
    while count <= len(plants_sorted):
        if plants_sorted[count].load != plants_sorted[count].pmax:
            if count - 1 < 0:
                return None
            else:
                return plants_sorted[count - 1]
        count += 1
    return None

def plant_price_lowest_cost_pmin(plants: list) -> Powerplant:
    plants_sorted = sorted(plants, key=lambda plant: plant.price_minimun_active)
    for plant in plants_sorted:
        if plant.load < plant.pmin:
            return plant
    return None

def best_conbination(load_inicial: float, plants: list) -> list:
    difference = load_inicial

    while difference > 0:
        lowest_plant = plant_most_efficient(plants)
        if lowest_plant is None:
            break
        
        if difference >= (lowest_plant.pmax - lowest_plant.load):
            lowest_plant.write_load(lowest_plant.pmax)
        
        elif difference >= lowest_plant.pmin:
            lowest_plant.write_load(difference + lowest_plant.load)
            
        else:
            previous_plant = plant_most_efficient_previous(plants)
            plant_activate = plant_price_lowest_cost_pmin(plants)
            
            if previous_plant is None:
                lowest_plant.write_load(lowest_plant.pmin)
            
            if previous_plant.pmax - previous_plant.pmin > lowest_plant.pmin:
                lowest_plant.write_load(lowest_plant.pmin)
                previous_plant.write_load(previous_plant.pmax - lowest_plant.pmin + difference)
            else:
                previous_plant.write_load(0)
                plant_activate.write_load(plant_activate.pmin)
                
        difference = load_inicial - sum([plant.load for plant in plants])

    response_float = [plant.load for plant in plants]
    name_plants = [plant.name for plant in plants]
    diccionary = [{'name': x, 'p': y} for x, y in zip(name_plants, response_float)]
    
    return diccionary
    


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
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'] * velocidad_viento, 0)
        elif plant['type'] == 'gasfired':
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_gas)
        elif plant['type'] == 'turbojet':
            instancia = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_kerosine)
        else:
            raise ValueError(f"Unknown Powerplant type: {plant['type']}")
        instancias.append(instancia)
    
    return load, instancias


#import json
#if __name__ == "__main__":
#    
#    with open("./example_payloads/payload3.json") as f:
#        data = json.load(f)
#    
#    process_json(data)