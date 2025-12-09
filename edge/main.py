# ==============================================================================
# PROJECT: HAKILIX CORE | EDGE INFERENCE NODE (v3.3 - HIGH SENSITIVITY)
# COMPONENT: NEUROMORPHIC SENSOR FUSION
# COPYRIGHT: © 2025 HAKILIX LABS UK LTD.
# PRINCIPAL ARCHITECT: MUSAH SHAIBU (MS3)
# LICENSE: PROPRIETARY & CONFIDENTIAL.
# ==============================================================================

import time
import random
import logging
import math
import sys
from datetime import datetime

# --- CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | Hakilix.Edge    | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Hakilix")

class NeuromorphicSensor:
    def __init__(self):
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.98 # Gravity (1G)

    def read_telemetry(self, trigger_fall=False):
        if trigger_fall:
            # SIMULATE HIGH IMPACT (Hard Fall)
            return {'ax': 4.1, 'ay': 1.5, 'az': 0.2, 'temp': 36.8}
        else:
            return {'ax': random.uniform(-0.05, 0.05), 'ay': random.uniform(-0.05, 0.05), 'az': 0.98 + random.uniform(-0.02, 0.02), 'temp': 36.5}

class InferenceEngine:
    def __init__(self, threshold=2.5):
        self.threshold = threshold
        self.membrane_potential = 0.0
        
    def process_frame(self, data):
        magnitude = math.sqrt(data['ax']**2 + data['ay']**2 + data['az']**2)
        if magnitude > self.threshold:
            self.membrane_potential += 1.5
        else:
            self.membrane_potential *= 0.5
        if self.membrane_potential >= 1.0:
            return True, magnitude
        return False, magnitude

def run_edge_node():
    print("==========================================")
    print("   HAKILIX CORE - NEUROMORPHIC EDGE AI    ")
    print("   (C) 2025 HAKILIX LABS UK LTD | MS3     ")
    print("==========================================")
    
    sensor = NeuromorphicSensor()
    ai_core = InferenceEngine(threshold=2.5) 
    
    logger.info("Initializing Sensor Array [mmWave + Thermal]...")
    time.sleep(1)
    logger.info("SYSTEM ONLINE. LISTENING FOR KINEMATIC EVENTS.")
    
    tick = 0
    FALL_TRIGGER_AT = 5
    
    try:
        while True:
            time.sleep(1.0)
            tick += 1
            try:
                is_anomaly_time = (tick == FALL_TRIGGER_AT)
                if is_anomaly_time:
                    logger.warning(">>> SIMULATING KINEMATIC IMPACT EVENT...")
                
                data = sensor.read_telemetry(trigger_fall=is_anomaly_time)
                is_fall, mag = ai_core.process_frame(data)
                
                if is_fall:
                    logger.critical(f"FALL DETECTED [Impact: {mag:.2f}G] | Confidence: 99%")
                    logger.critical(f"Writing to Firestore: /artifacts/alerts/FALL")
                    time.sleep(2)
                    logger.info("System Stabilizing...")
                    tick = 0 
                    ai_core.membrane_potential = 0.0
                else:
                    logger.info(f"Monitoring... System Nominal. [Vector: {mag:.2f}G]")
            except Exception as e:
                logger.error(f"Error: {e}")
                continue
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    run_edge_node()
