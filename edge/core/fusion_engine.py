import logging
from edge.config import config
from edge.core.snn_network import SpikingNetwork

logger = logging.getLogger("Hakilix.Fusion")

class FusionEngine:
    def __init__(self):
        self.snn = SpikingNetwork()
        self.state = "MONITORING"

    def process(self, radar_data, thermal_data):
        """
        The Central Intelligence of the Edge Node.
        Fuses data and passes it through the SNN.
        """
        # 1. Extract Features
        v_z = radar_data.get('velocity', 0.0)
        acc = radar_data.get('acceleration', 0.0)
        t_var = thermal_data.get('variance', 0.0)
        
        # 2. Neuromorphic Inference
        # We pass the raw sensor values into the LIF neurons
        spike_detected = self.snn.infer(v_z, acc, t_var)
        
        # 3. Decision Logic
        if spike_detected:
            # Double check thresholds (Safety Layer)
            if v_z > config.FALL_VELOCITY_LIMIT:
                logger.critical(f"FALL DETECTED! Velocity={v_z:.2f} m/s")
                return "CRITICAL_ALERT"
            
        return "SAFE"