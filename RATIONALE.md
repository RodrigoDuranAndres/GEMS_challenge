## Methods Advance

In the code [methods_advance.py](app/utils/methods_advance.py), is where the calculations take place.

### Dicontinuity

def best_combination
The first problem face is that some powerplant don't accept all load so its posible load are 0 & pmin-pmax.
To addres this, the powerplants that have this discotunuity may apper (case: load in range pmin-pmax) or not apper (case: load is 0) from the subset.

### Efficient Combination

def best_solution_plants
All the power plants of the subset that is pass its load has to be in between pmin-pmax. So we charge to the minumum all the powerplants, and the reamining load is assigned by eficiency. (price_energy_unit)

## Edge Cases

In the case that the load is imposible to reach it send back an error.
In the case the load is imposible to reach but one that is higher is, this higher solution will be the one send back.
