import numpy as np
from matplotlib import pyplot as plt

class FlowerSpecies:
    def __init__(self, colour, pollen=1):
        self.colour = colour
        self.pollen = pollen

class Flower:
    def __init__(self, c, pol, pos, size=3):
        self.col = c
        self.pol = pol
        self.pos = pos
        self.size = size


ROSE = FlowerSpecies("r")

def new_flower(species, x, y):
    return Flower(species.colour, species.pollen, np.array([x, y]))
