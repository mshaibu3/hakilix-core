import logging
from edge.core.lif_neuron import LIFNeuron
logger = logging.getLogger("Hakilix.SNN")

class SpikingNetwork:
    def __init__(self):
        self.neurons = {
            'velocity': LIFNeuron(0),
            'accel': LIFNeuron(1),
            'thermal': LIFNeuron(2)
        }

    def infer(self, radar_velocity, radar_accel, thermal_variance):
        spikes = {
            'v': self.neurons['velocity'].step(radar_velocity),
            'a': self.neurons['accel'].step(radar_accel),
            't': self.neurons['thermal'].step(thermal_variance)
        }
        is_critical = (spikes['v'] == 1) and (spikes['t'] == 1)
        if is_critical:
            logger.info(f"SNN COINCIDENCE DETECTED: Spikes={spikes}")
        return is_critical