import asyncio
import logging
import random
from edge.config import config

logger = logging.getLogger("Hakilix.Radar")

class RadarDriver:
    def __init__(self):
        self.connected = False

    async def connect(self):
        if config.SIMULATE_SENSORS:
            logger.info(f"[SIM] Radar IWR6843 initialized (Virtual Port).")
            self.connected = True
            return
        
        # Physical connection logic would go here (using pyserial)
        logger.info(f"Connecting to Radar at {config.RADAR_PORT}...")
        await asyncio.sleep(1)
        self.connected = True

    async def get_frame(self):
        """
        Returns a dict containing:
        - point_cloud: list of (x,y,z,v) tuples
        - target_velocity: float (m/s)
        """
        if not self.connected: return {'velocity': 0.0, 'acceleration': 0.0}
        
        if config.SIMULATE_SENSORS:
            # Synthetic Data Generation
            await asyncio.sleep(0.1) # 10Hz
            
            # 1% chance of high velocity (simulating a fall)
            is_fall = random.random() > 0.99
            velocity = random.uniform(2.5, 4.0) if is_fall else random.uniform(0.0, 0.5)
            
            return {
                "velocity": velocity,
                "acceleration": velocity / 0.1, # Simplified physics
                "num_points": 15 if is_fall else 3
            }
        return {'velocity': 0.0, 'acceleration': 0.0}