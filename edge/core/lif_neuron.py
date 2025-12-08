import numpy as np
from edge.config import config

class LIFNeuron:
    def __init__(self, neuron_id: int):
        self.id = neuron_id
        self.v_mem = config.LIF_REST
        self.spike = 0
    
    def step(self, input_current: float) -> int:
        self.v_mem = self.v_mem * config.LIF_DECAY + input_current
        if self.v_mem >= config.LIF_THRESHOLD:
            self.spike = 1
            self.v_mem = config.LIF_REST
        else:
            self.spike = 0
        return self.spike