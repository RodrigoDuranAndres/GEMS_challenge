from utils.classes import *
import itertools

def process_json(data):
    """
    Process the data from a json file and return the best combination of powerplants as a dictionary

    The function read the data from a json file, and then use the function best_combination
    to obtain the best combination of powerplants that can generate the load required
    and finally return the response as a dictionary.

    Parameters
    ----------
    data : dict
        A dictionary with the data from the json file

    Returns
    -------
    dict
        A dictionary with the response
    """
    objective, plants = read_json(data)
    response = best_combination(objective, plants)
    diccionary = structure_response(response, plants)

    return diccionary

def structure_response(response, plants):
    """
    Process the response from best_combination and return a dictionary with the name of each powerplant and its load

    Parameters
    ----------
    response : dict
        A dictionary with the name of each powerplant and its load
    plants : list
        A list of Powerplant objects

    Returns
    -------
    dict
        A dictionary with the name of each powerplant and its load
    """
    for plant, load in response.items():
        plant.load = load

    plant_loads = [plant.load for plant in plants]
    plant_names = [plant.name for plant in plants]
    response_dict = [{'name': name, 'p': load} for name, load in zip(plant_names, plant_loads)]

    return response_dict

def best_combination(load_inicial: float, plants: list) -> list:
    """
    Find the best combination of powerplants to generate the required load.
    To adrees the dicotinuity, originated by pmin of the powerplants, we use the itertools library,
    this way we create subset of continuous options, that are pocesed indibidualy by the best_solution_plants function.
    It stores and finally send the best option.

    Parameters
    ----------
    load_inicial : float
        The required load
    plants : list
        A list of Powerplant objects

    Returns
    -------
    list
        A list of dictionaries that as key has the power plant object and as value its load, with the best combination
    """
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
    """
    Find the best combination of powerplants to generate the required load
    This function takes the list of powerplants and the required load, and returns
    a tuple with the status, the cost of the solution and a dictionary with the name of each plant and its load.

    Parameters
    ----------
    load_inicial : float
        The required load
    plants : list
        A list of Powerplant objects

    Returns
    -------
    Tuple:
        The status:
            -1 if the solution is not posible
            0 if the solution is good
            1 if the production exccedits the load
        The cost of the solution
        A dictionary with the name of each powerplant and its load
    """
    
    # Make sure there are powerplants
    if len(plants) == 0:
        return -1, None, None
    
    # Make sure there is enough to reach the load
    sum_plants_maximun = sum([plant.pmax for plant in plants])
    if sum_plants_maximun < load_inicial:
        return -1, None, None
    
    load = load_inicial
    plants_load = {plant: plant.pmin for plant in plants}
    
    # We asign the minimun load to enter the space of posibilities of this subset where all the power plants are activated
    sum_plants_minimun = sum([plant.pmin for plant in plants])
    load -= sum_plants_minimun
    
    # Iterate to asign the reamining load with preference for the most eficients power plants
    plants_sorted = sorted(plants, key=lambda plant: plant.price_energy_unit)
    while load > 0:
        plant = plants_sorted.pop(0)
        if plants_load[plant] + load < plant.pmax:
            plants_load[plant] += load
            load = 0
        else:
            load -= (plant.pmax - plants_load[plant])
            plants_load[plant] = plant.pmax
    
    # Calculate the cost
    costo_total = 0
    for plant in plants:
        costo_total += plant.price_energy_unit * plants_load[plant]

    # Check if the production exccedits the load
    if load < 0:
        return 1, costo_total, plants_load
    else:
        return 0, costo_total, plants_load

def read_json(data):
    """
    Read the data from a json file and return the load and the list of powerplants objects.

    Parameters
    ----------
    data : dict
        A dictionary with the data from the json file

    Returns
    -------
    tuple
        A tuple with the load and the list of powerplants
    """

    load = data["load"]
    fuels = data["fuels"]
    Powerplants = data["powerplants"]
    
    velocidad_viento = fuels["wind(%)"] / 100
    price_gas = fuels["gas(euro/MWh)"]
    price_kerosine = fuels["kerosine(euro/MWh)"]
    price_co2 = fuels["co2(euro/ton)"]
    
    instances = []
    for plant in Powerplants:
        if plant['type'] == 'windturbine':
            instance = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'] * velocidad_viento)
        elif plant['type'] == 'gasfired':
            instance = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_gas, price_co2 = price_co2)
        elif plant['type'] == 'turbojet':
            instance = Powerplant(plant['name'], plant['type'], plant['efficiency'], plant['pmin'], plant['pmax'], price_kerosine)
        else:
            raise ValueError(f"Unknown Powerplant type: {plant['type']}")
        instances.append(instance)
    
    return load, instances
