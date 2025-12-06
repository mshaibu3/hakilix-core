import asyncio
import logging
import random
from edge.config import config

logger = logging.getLogger("Hakilix.Thermal")

class ThermalDriver:
    def __init__(self):
        self.connected = False

    async def connect(self):
        if config.SIMULATE_SENSORS:
            logger.info("[SIM] FLIR Lepton initialized (Virtual SPI).")
            self.connected = True
            return
        
        logger.info("Initializing FLIR Lepton...")
        await asyncio.sleep(0.5)
        self.connected = True

    async def get_frame(self):
        """
        Returns a dict containing radiometric data.
        """
        if not self.connected: return {'variance': 0.0}
        
        if config.SIMULATE_SENSORS:
            await asyncio.sleep(0.1)
            # Simulate heat variance (person moving vs static background)
            variance = random.uniform(0.1, 0.9)
            return {
                "max_temp": 36.5,
                "variance": variance,
                "status": "nominal"
            }
        return {'variance': 0.0}