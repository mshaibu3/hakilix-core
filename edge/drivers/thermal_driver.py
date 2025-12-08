import asyncio
import logging
import random
from edge.config import config
logger = logging.getLogger("Hakilix.Thermal")

class ThermalDriver:
    def __init__(self): self.connected = False
    async def connect(self):
        logger.info("[SIM] FLIR Lepton initialized.")
        self.connected = True
    async def get_frame(self):
        await asyncio.sleep(0.1)
        return {"max_temp": 36.5, "variance": random.uniform(0.1, 0.9)}