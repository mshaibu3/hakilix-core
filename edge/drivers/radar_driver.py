import asyncio
import logging
import random
from edge.config import config
logger = logging.getLogger("Hakilix.Radar")

class RadarDriver:
    def __init__(self): self.connected = False
    async def connect(self):
        logger.info(f"[SIM] Radar IWR6843 initialized.")
        self.connected = True
    async def get_frame(self):
        await asyncio.sleep(0.1)
        is_fall = random.random() > 0.99
        velocity = random.uniform(2.5, 4.0) if is_fall else random.uniform(0.0, 0.5)
        return {"velocity": velocity, "acceleration": velocity/0.1}