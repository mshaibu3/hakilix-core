import asyncio
import logging
import signal
import sys
from edge.utils.logger import setup_logger
from edge.config import config
from edge.drivers.radar_driver import RadarDriver
from edge.drivers.thermal_driver import ThermalDriver
from edge.core.fusion_engine import FusionEngine

logger = setup_logger("Hakilix.Main")

class EdgeNode:
    def __init__(self):
        self.running = True
        self.radar = RadarDriver()
        self.thermal = ThermalDriver()
        self.fusion = FusionEngine()

    async def startup(self):
        # Fixed ASCII art formatting using raw string with single quotes to avoid syntax errors
        print(r'''
   __  _____    __  _____    _____  __
  / / / /   |  / / / /  |  / /   |/ /
 / /_/ / /| | / / / // /| / / /|   / 
/ __  / ___ |/ /___/ ___ / /___/   |  
/_/ /_/_/  |_/____/_/  |_/____/_/|_|  
        ''')
        logger.info(f"Booting Hakilix Core v1.0.4 | Device: {config.DEVICE_ID}")
        logger.info(f"Mode: {'SIMULATION' if config.SIMULATE_SENSORS else 'PRODUCTION'}")
        
        await asyncio.gather(self.radar.connect(), self.thermal.connect())
        logger.info("Sensors Online. Starting Active Inference Loop...")

    async def loop(self):
        while self.running:
            try:
                # 1. Async Data Acquisition
                r_data, t_data = await asyncio.gather(
                    self.radar.get_frame(),
                    self.thermal.get_frame()
                )
                
                # 2. Fusion & Inference
                status = self.fusion.process(r_data, t_data)
                
                # 3. Cloud Sync (Placeholder for MQTT publish)
                if status == "CRITICAL_ALERT":
                    logger.info(">> Uploading encrypted alert packet to AWS IoT...")
                
            except Exception as e:
                logger.error(f"Runtime Exception: {e}")
                await asyncio.sleep(1)

    async def shutdown(self):
        logger.warning("Shutdown Signal Received.")
        self.running = False

if __name__ == "__main__":
    node = EdgeNode()
    
    # Graceful Exit Handling for Windows/Linux
    if sys.platform != 'win32':
        loop = asyncio.new_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(node.shutdown()))
        asyncio.set_event_loop(loop)
    else:
        # Standard Python 3.10+ startup (Windows fix)
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        except Exception:
            loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(node.startup())
        loop.run_until_complete(node.loop())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()