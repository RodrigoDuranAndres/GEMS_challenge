# Use 

This is an app is feed payloads (like the ones in example payloads that contains)
Its a solution to the challenge from [GEMS](https://github.com/gems-st-ib/powerplant-coding-challenge)

## Execution

Make sure you have your  Docker Engine Runnning, then built up the docker volume 
```
docker build -t flask-app ./app/
```
Create an image from the docker volumne, route the port 8808
```
docker run -p 8808:8808 flask-app
```

## Usage 

You have a python example of the usage in [example_usage.py](example_usage.py).
You have to send your payload to 'http://localhost:8808/productionplan'

## Loads of the proyect

#### Payload

You can find examples in example_payloads/*
The payload contains 3 types of data:
 - load: The load is the amount of energy (MWh) that need to be generated during one hour.
 - fuels: based on the cost of the fuels of each powerplant, the merit-order can be determined which is the starting point for deciding which powerplants should be switched on and how much power they will deliver.  Wind-turbine are either switched-on, and in that case generate a certain amount of energy depending on the % of wind, or can be switched off. 
   - gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
   - kerosine(euro/Mwh): the price of kerosine per MWh.
   - co2(euro/ton): the price of emission allowances (optionally to be taken into account).
   - wind(%): percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
 - powerplants: describes the powerplants at disposal to generate the demanded load. For each powerplant is specified:
   - name:
   - type: gasfired, turbojet or windturbine.
   - efficiency: the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
   - pmax: the maximum amount of power the powerplant can generate.
   - pmin: the minimum amount of power the powerplant generates when switched on. 

#### Response

You can find examples in example_outputs/*
The reponse contains 2 types of data
- name: name of the power plant
- p: is the energy producio
