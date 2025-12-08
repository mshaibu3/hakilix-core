import asyncio
import logging
import signal
import sys
import json
from edge.utils.logger import setup_logger
from edge.config import config
from edge.drivers.radar_driver import RadarDriver
from edge.drivers.thermal_driver import ThermalDriver
from edge.core.fusion_engine import FusionEngine
from edge.core.home_bridge import HomeBridge

logger = setup_logger("Hakilix.Main")

class EdgeNode:
    def __init__(self):
        self.running = True
        self.radar = RadarDriver()
        self.thermal = ThermalDriver()
        self.fusion = FusionEngine()
        self.bridge = HomeBridge()

    async def startup(self):
        print("==========================================")
        print("   HAKILIX CORE - NEUROMORPHIC EDGE AI    ")
        print("==========================================")
        logger.info(f"Booting Hakilix Core v2.0.0 | Device: {config.DEVICE_ID}")
        await asyncio.gather(self.radar.connect(), self.thermal.connect())
        logger.info("Sensors Online. Starting Neuromorphic Loop...")

    async def loop(self):
        while self.running:
            try:
                r_data, t_data = await asyncio.gather(self.radar.get_frame(), self.thermal.get_frame())
                status = self.fusion.process(r_data, t_data)
                if status == "CRITICAL_ALERT":
                    fhir = self.bridge.convert_to_fhir(status, 0.95)
                    logger.info(f">> Sending FHIR Packet: {json.dumps(fhir)}")
            except Exception as e:
                logger.error(f"Runtime Exception: {e}")
                await asyncio.sleep(1)

    async def shutdown(self):
        logger.warning("Shutdown Signal Received.")
        self.running = False

if __name__ == "__main__":
    node = EdgeNode()
    if sys.platform != 'win32':
        loop = asyncio.new_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(node.shutdown()))
        asyncio.set_event_loop(loop)
    else:
        try: loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        except Exception: loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(node.startup())
        loop.run_until_complete(node.loop())
    except KeyboardInterrupt: pass
    finally: loop.close()