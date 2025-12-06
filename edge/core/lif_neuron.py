import numpy as np
from edge.config import config

class LIFNeuron:
    """
    Leaky Integrate-and-Fire (LIF) Neuron Model.
    
    Mathematical Model:
    dV/dt = -(V - V_rest)/tau + I_in
    
    This class implements a discrete-time approximation for Edge AI inference.
    """
    def __init__(self, neuron_id: int):
        self.id = neuron_id
        self.v_mem = config.LIF_REST  # Membrane potential
        self.spike = 0                 # Output spike (0 or 1)
    
    def step(self, input_current: float) -> int:
        """
        Process one time-step.
        
        Args:
            input_current (float): Normalized input signal (e.g., Radar Velocity).
            
        Returns:
            int: 1 if spike fired, 0 otherwise.
        """
        # 1. Integrate (Leak)
        self.v_mem = self.v_mem * config.LIF_DECAY + input_current
        
        # 2. Fire
        if self.v_mem >= config.LIF_THRESHOLD:
            self.spike = 1
            # 3. Reset (Hard reset)
            self.v_mem = config.LIF_REST
        else:
            self.spike = 0
            
        return self.spike

    def reset(self):
        self.v_mem = config.LIF_REST
        self.spike = 0