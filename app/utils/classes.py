class Powerplant:
    def __init__(self, name: str, tipe: str, efficiency: float, pmin: int, pmax: int, price: float = 0, price_co2: float = 0):
        self.name = name
        self.tipe = tipe
        self.efficiency = efficiency
        self.pmin = pmin
        self.pmax = pmax
        self.price = price
        self.price_energy_unit = self.price * (1/self.efficiency) + 0.3 * price_co2
        self.price_minimun_active = self.price_energy_unit * self.pmin
        self.load = 0
    
    def write_load(self, load: int):
        if self.pmin <= load <= self.pmax or load == 0:
            self.load = load
        else:
            raise ValueError("Invalid load")
        
    def __str__(self) -> str:
        return f"Poweplant: {self.name} ({self.tipe}) - efficiency: {self.efficiency:.2f} - Cost per MWh: {self.price_energy_unit}"
