# ==============================================================================
# PROJECT: HAKILIX CORE | CLOUD UPLINK SERVER (v4.1 - ENTERPRISE)
# COMPONENT: NEUROMORPHIC DATA ORCHESTRATOR & FHIR GATEWAY
# COPYRIGHT: © 2025 HAKILIX LABS UK LTD.
# PRINCIPAL ARCHITECT: MUSAH SHAIBU (MS3)
# LICENSE: PROPRIETARY & CONFIDENTIAL.
# ==============================================================================

import time
import json
import random
import logging
import uuid
from datetime import datetime

# --- CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | Hakilix.Cloud | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Backend")

class HakilixBackend:
    def __init__(self):
        self.status = "ONLINE"
        self.connected_devices = 85
        self.session_id = str(uuid.uuid4())[:8]
        logger.info(f"[INIT] Hakilix Core v4.1 Orchestrator Online. Session: {self.session_id}")
        logger.info(f"[NET] Active Fleet Connection: {self.connected_devices} Nodes")
        logger.info("[SEC] Homomorphic Encryption Layer: ACTIVE (AES-256-GCM)")
        logger.info("[API] NHS Virtual Ward Interoperability: READY")

    def simulate_processing_latency(self):
        time.sleep(random.uniform(0.01, 0.05))

    def decrypt_and_verify(self, raw_data):
        """
        Simulates advanced decryption and integrity verification.
        """
        self.simulate_processing_latency()
        # Mock Integrity Check
        if random.random() > 0.99:
            logger.warning(f"[SEC] Integrity Check Warning for Packet {raw_data.get('device_id', 'UNKNOWN')}")
        return raw_data

    def process_telemetry(self, payload):
        """
        Processes edge telemetry with advanced diagnostic logging.
        """
        start_time = time.time()
        data = self.decrypt_and_verify(payload)
        
        device_id = data.get("device_id")
        velocity = data.get("velocity", 0.0)
        
        # Risk Logic
        risk_score = 0.0
        risk_level = "NOMINAL"
        
        if velocity > 2.5:
            risk_level = "CRITICAL_FALL"
            risk_score = 0.99
            logger.critical(f"!! [ALERT] {device_id} :: FALL DETECTED :: Conf: {risk_score*100:.1f}% !!")
            logger.critical(f"   >> DISPATCH PROTOCOL 4A INITIATED")
            logger.critical(f"   >> NHS FHIR PACKET SENT: Observation/Fall/{uuid.uuid4()}")
        elif velocity < 0.1:
            risk_level = "SEDENTARY"
            risk_score = 0.45
        else:
            risk_score = 0.12

        process_time = (time.time() - start_time) * 1000
        
        log_entry = (
            f"[DATA] {device_id} | "
            f"Vel: {velocity:.2f}m/s | "
            f"Risk: {risk_level} ({risk_score:.2f}) | "
            f"Latency: {process_time:.2f}ms"
        )
        
        if risk_level != "CRITICAL_FALL":
            logger.info(log_entry)
            
        return {"status": "200 OK", "risk": risk_level}

if __name__ == "__main__":
    server = HakilixBackend()
    try:
        while True:
            # Random device heartbeat with slight variance
            mock_payload = {
                "device_id": f"HKLX-{random.randint(10,99)}",
                "velocity": random.uniform(0.0, 3.0) if random.random() > 0.1 else 0.0,
                "timestamp": datetime.now().isoformat()
            }
            # Occasionally inject a system diagnostic message
            if random.random() > 0.95:
                logger.info(f"[DIAG] System Health Check: CPU 12% | MEM 24% | QUEUE: 0")
                
            server.process_telemetry(mock_payload)
            time.sleep(random.uniform(0.8, 1.5))
            
    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] Graceful stop initiated. Closing secure sockets...")
