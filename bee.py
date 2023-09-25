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
        self.bias = s.BETA
        self.pos = start.copy()
        self.dir = theta
        self.dir_change = 0
        self.delta = delta
        self.hungry_in = 0

    def take_step(self, flowers=[]):
        self.update_heading(flowers)
        self.dir += self.dir_change
        self.pos += np.array([np.cos(self.dir), np.sin(self.dir)]) * s.DELTA
        self.wrap_pos()
        #return np.array([np.cos(self.dir), np.sin(self.dir)])

    def update_heading(self, flowers):
        self.hungry_in -= 1
        fe = self.flower_effect(flowers) if self.hungry_in <= 0 else 0
        ce = self.control_effect()
        ne = self.noise_effect()
        effects = np.array([fe, ce, ne])
        
        strengths = np.array([s.CHI, s.GAMMA, s.ETA])
        strengths = strengths / sum(strengths)

        self.dir_change = effects.dot(strengths)

    def wrap_pos(self):
        if self.pos[0] > s.MAX_XLIM:
            self.pos[0] = s.MAX_XLIM
        elif self.pos[0] < s.MIN_XLIM:
            self.pos[0] = s.MIN_XLIM
        if self.pos[1] > s.MAX_YLIM:
            self.pos[1] = s.MAX_YLIM
        elif self.pos[1] < s.MIN_YLIM:
            self.pos[1] = s.MIN_YLIM

    def flower_effect(self, flowers):
        if len(flowers) < 1:
            return 0
        v_flowers = np.array([f.pos for f in flowers])

        eff = np.zeros(2)
        deltas = np.concatenate(v_flowers) - np.repeat(self.pos, len(v_flowers))
        deltas = np.reshape(deltas, [len(v_flowers), 2])

        delta_mags = np.linalg.norm(deltas, axis=1)
        close_enough = delta_mags < s.VIEW_RADIUS
    
        if np.any(delta_mags < s.FEEDING_DISTANCE):
            self.hungry_in = s.HUNGRY_TIME
            print("HIT")

        delta_normed = (deltas.T / delta_mags).T
        heading = np.array([np.cos(self.dir-s.VIEW_ARC), np.sin(self.dir-s.VIEW_ARC)])
        unit_heading = heading / np.linalg.norm(heading)
    
        headings = np.arccos(np.sum(unit_heading * delta_normed, axis=1))
        visible_flowers = v_flowers[np.logical_and(headings < (2*s.VIEW_ARC), close_enough)]
        visible_flowers = np.logical_and(headings < (2*s.VIEW_ARC), close_enough)
        
        if sum(visible_flowers) >= 1:
            self.bias = s.SEEKING_BETA
            exp_deltas = np.exp(np.linalg.norm(deltas[visible_flowers], axis=1))
            exp_total = sum(exp_deltas)
    
            cum_delta = (deltas[visible_flowers] * np.reshape(exp_deltas, [len(exp_deltas), 1])) / exp_total
            normed_delta = (cum_delta / np.linalg.norm(cum_delta))[0]
            
            if abs(np.sum(normed_delta + unit_heading)) <= 0.001:
                return 0
            v = (np.arccos(normed_delta.dot(unit_heading)) - np.pi)
            return v
        else:
            self.bias = s.BETA
            return 0
            

    def control_effect(self):
        if self.dir_change == 0:
            bias = 0.5
        else:
            bias = self.bias

        obey_bias = np.random.random() <= bias
        #control = np.random.random()
        control = np.pi/16

        if self.dir_change <= 0:
            self.dir_change = (-1 if obey_bias else 1) * control
        else:
            self.dir_change = (1 if obey_bias else -1) * control
        
        # return a change in theta
        return self.dir_change

    def noise_effect(self):
        return (np.random.random() * 2 - 1) * s.ETA
        
