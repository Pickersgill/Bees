import numpy as np
import style as s, flower
from matplotlib import pyplot as plt, animation

class Bee:
    """
    theta : heading
    eta : noise effect
    gamma : control effect
    beta : control bias
    delta : speed
    """
    def __init__(self, start, theta, eta, gamma, beta, delta):
        self.e = eta
        self.g = gamma
        self.b = beta
        self.pos = start.copy()
        self.dir = theta
        self.dir_change = 0
        self.delta = delta

    def take_step(self, flowers=[]):
        c = self.control_effect() * s.GAMMA
        f = self.flower_effect(flowers) * s.CHI
        self.pos += (c + f) * s.DELTA
        self.wrap_pos()

    def wrap_pos(self):
        if self.pos[0] > s.MAX_XLIM:
            self.pos[0] = s.MIN_XLIM
        elif self.pos[0] < s.MIN_XLIM:
            self.pos[0] = s.MAX_XLIM
        if self.pos[1] > s.MAX_YLIM:
            self.pos[1] = s.MIN_YLIM
        elif self.pos[1] < s.MIN_YLIM:
            self.pos[1] = s.MAX_YLIM

    def flower_effect(self, flowers):
        if flowers:
            eff = np.zeros(2)
            deltas = np.concatenate(np.array([f.pos for f in flowers])) - \
                    np.repeat(self.pos, len(flowers))
            deltas = np.reshape(deltas, [len(flowers), 2])
        
            exp_deltas = np.exp(np.linalg.norm(deltas, axis=1))
            exp_total = sum(exp_deltas)

            cum_delta = (deltas * np.reshape(exp_deltas, [len(exp_deltas), 1])) / exp_total
            normed_delta = cum_delta / np.linalg.norm(cum_delta)
            return sum(normed_delta)
            
        return np.zeros(2)

    def control_effect(self):
        if self.dir_change == 0:
            bias = 0.5
        else:
            bias = self.b

        obey_bias = np.random.random() <= bias
        control = np.random.random()
        noise = (np.random.random() * 2 - 1) * self.e

        if self.dir_change <= 0:
            self.dir_change = (-1 if obey_bias else 1) * control
        else:
            self.dir_change = (1 if obey_bias else -1) * control
        self.dir += self.dir_change + noise

        return np.array([np.cos(self.dir), np.sin(self.dir)])
