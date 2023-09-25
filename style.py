import numpy as np

BEE_COUNT = 10

ETA = 0.2 # Noise effect
GAMMA = 8 # Control effect
BETA = 0.9 # Turn bias
SEEKING_BETA = 0.5 # Bias whilst seeking flower
DELTA = 0.1 # Speed 
STEPS = 10 # DEP. Animation steps
CHI = 0.5 # Flower effect

# Control effect in range 10**1 times flower effect smooths loops. 

VIEW_RADIUS=20
VIEW_ARC=np.pi

LINE_COL = "k"
LINE_MARKER = "o"
LINE_STYLE = LINE_COL + LINE_MARKER
MEMORY = 100

MIN_XLIM = -10
MAX_XLIM = -MIN_XLIM

MIN_YLIM = MIN_XLIM
MAX_YLIM = -MIN_YLIM

FEEDING_DISTANCE = 0.5
HUNGRY_TIME = 350
