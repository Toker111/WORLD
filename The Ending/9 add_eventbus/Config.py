from dataclasses import dataclass
import mypy

@dataclass
class WorldConfig():
    size:int = 8
    initial_food:int = 8
    number_of_organisms:int = 8
@dataclass
class OrganismConfig():
    energy:int = 100
    food_energy:int = 30
    energy_to_reproduct:int = 150
