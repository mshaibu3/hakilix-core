import logging
from edge.core.lif_neuron import LIFNeuron

logger = logging.getLogger("Hakilix.SNN")

class SpikingNetwork:
    """
    A simple Feed-Forward Spiking Neural Network (SNN) for Fall Detection.
    Maps continuous sensor data into temporal spike trains.
    """
    def __init__(self):
        # Layer 1: Encoding Neurons (Velocity, Acceleration, ThermalVariance)
        self.neurons = {
            'velocity': LIFNeuron(0),
            'accel': LIFNeuron(1),
            'thermal': LIFNeuron(2)
        }
        self.spike_history = []

    def infer(self, radar_velocity, radar_accel, thermal_variance):
        """
        Run inference on the current frame.
        """
        # Normalize inputs
        spikes = {
            'v': self.neurons['velocity'].step(radar_velocity),
            'a': self.neurons['accel'].step(radar_accel),
            't': self.neurons['thermal'].step(thermal_variance)
        }
        
        # Temporal Coincidence Detection (Simple Hebbian Logic)
        # If Velocity and Thermal neurons spike simultaneously -> CRITICAL EVENT
        is_critical = (spikes['v'] == 1) and (spikes['t'] == 1)
        
        if is_critical:
            logger.info(f"SNN COINCIDENCE DETECTED: Spikes={spikes}")
            
        return is_critical