class PlantaEnergia:
    def __init__(self, nombre: str, tipo: str, eficiencia: float, pmin: int, pmax: int, precio: float):
        self.nombre = nombre
        self.tipo = tipo
        self.eficiencia = eficiencia
        self.pmin = pmin
        self.pmax = pmax
        self.precio = precio
        self.precio_unidad_energia = self.precio * (1/self.eficiencia)
        self.precio_minimo_activa = self.precio_unidad_energia * self.pmin
        self.carga = 0
    
    def write_carga(self, carga: int):
        if self.pmin <= carga <= self.pmax:
            self.carga = carga
        else:
            raise ValueError("Carga inválida")
        
    def __str__(self) -> str:
        return f"Planta de energía {self.nombre} ({self.tipo}) - Eficiencia: {self.eficiencia:.2f} - Coste energia: {self.precio_unidad_energia}"
        
