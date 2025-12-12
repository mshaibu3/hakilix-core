import time, random, logging, requests, os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Hakilix")
BACKEND_URL = f"{os.environ.get('CLOUD_URL', 'http://localhost:8080')}/api/ingest"
DEVICE_ID = "HKLX-01"

def run():
    print("--- HAKILIX EDGE SENSOR ACTIVE ---")
    while True:
        try:
            accel_z = 0.98 + random.uniform(-0.05, 0.05)
            is_fall_sim = False
            
            if random.random() > 0.95:
                accel_z = 4.1
                is_fall_sim = True
                logger.warning(f"SIMULATING IMPACT: {accel_z:.2f}G")

            frame = {
                "timestamp": datetime.now().isoformat(),
                "vertical_accel_g": accel_z,
                "posture_angle_deg": 90.0 if not is_fall_sim else 0.0,
                "movement_energy": 0.5 if not is_fall_sim else 2.5,
                "zone": "living_room",
                "is_in_bed": False,
                "step_rate_hz": 1.2
            }
            
            requests.post(BACKEND_URL, json={"patient_id": DEVICE_ID, "frames": [frame]}, timeout=1)
            time.sleep(1.0)
            
        except KeyboardInterrupt: break
        except Exception as e: pass; time.sleep(2)

if __name__ == "__main__": run()